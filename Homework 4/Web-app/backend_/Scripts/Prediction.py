import time

import numpy as np
import pandas as pd
from keras import Sequential, Input
from keras.callbacks import EarlyStopping
from keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, mean_absolute_percentage_error, \
    mean_squared_log_error, explained_variance_score
from sklearn.preprocessing import MinMaxScaler
from Database.Database import Database

lag = 10


# This class is used for training the LSTM model and predicting future prices and saving them to the database
class Prediction:
    _db = Database()  # This class acts like a Database, which is used for saving and reading csv files

    def _pre_process(self, issuer):  # Makes a lag and adds SMA, EMA and STD to the data
        data = self._db.read(issuer, 'std')
        df = data[['Date', 'Last trade price']].copy()
        df['Date'] = pd.to_datetime(df['Date'], errors="coerce")
        df.set_index('Date', inplace=True)
        sma = df['Last trade price'].rolling(window=14).mean()
        ema = df['Last trade price'].ewm(span=14, adjust=False).mean()
        std = df['Last trade price'].rolling(window=14).std()
        periods = range(lag, 0, -1)

        for period in periods:
            df[f'Last_{period}'] = df['Last trade price'].shift(period)

        df['SMA'] = sma
        df['EMA'] = ema
        df['STD'] = std
        df.dropna(inplace=True)
        return df

    def _LSTM_MODEL(self, data):  # Trains the model
        X, Y = data.drop(columns=['Last trade price']), data['Last trade price']

        train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.3, shuffle=False)

        scaler_X = MinMaxScaler()
        train_X = scaler_X.fit_transform(train_X)
        test_X = scaler_X.transform(test_X)

        scaler_Y = MinMaxScaler()
        train_Y = scaler_Y.fit_transform(train_Y.to_numpy().reshape(-1, 1))

        train_X = train_X.reshape(train_X.shape[0], lag + 3,
                                  (train_X.shape[1] // lag))  # (samples, timesteps, features)
        test_X = test_X.reshape(test_X.shape[0], lag + 3, (test_X.shape[1] // lag))

        model = Sequential([
            Input((train_X.shape[1], train_X.shape[2],)),
            LSTM(64, activation="relu", return_sequences=True),
            Dropout(0.2),
            LSTM(16, activation="relu"),
            Dense(1, activation="linear")
        ])

        model.summary()

        model.compile(
            loss="mean_squared_error",
            optimizer="adam",
            metrics=["mean_squared_error"],
        )

        early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        history = model.fit(train_X, train_Y, validation_split=0.3, epochs=100, batch_size=16, shuffle=False,
                            callbacks=[early_stopping])

        pred_Y = model.predict(test_X)

        pred_Y = scaler_Y.inverse_transform(pred_Y)

        metrics = pd.DataFrame(
            columns=['r2_score', 'Mean Squared Error', 'Mean Absolute Error', 'Mean Absolute Percentage Error',
                     'Mean Squared Log Error', 'Explained Variance Score'])
        metrics.loc[len(metrics)] = [round(r2_score(test_Y, pred_Y), 2),
                                     round(mean_squared_error(test_Y, pred_Y), 2),
                                     round(mean_absolute_error(test_Y, pred_Y), 2),
                                     round(mean_absolute_percentage_error(test_Y, pred_Y), 2),
                                     round(mean_squared_log_error(test_Y, pred_Y), 2),
                                     round(explained_variance_score(test_Y, pred_Y), 2)]

        return [model, scaler_X, scaler_Y, data, metrics]

    def _LSTM_recursive_prediction(self, model, df, scaler_X, scaler_Y, n_days=10, lookback=10):
        # This uses a lookback, so it looks x-days back and use those to make prediction

        df_future = df.copy()
        future_predictions = pd.DataFrame(columns=['Date', 'Last trade price'])

        for _ in range(n_days):
            last_window = df_future.iloc[-lookback:].copy() # take the lookback window

            scaled = scaler_X.transform(last_window.drop(columns=['Last trade price'])) # Scale
            scaled = scaled.reshape(scaled.shape[0], lag + 3, (scaled.shape[1] // lag))
            pred_scaled = model.predict(scaled)
            pred_price = scaler_Y.inverse_transform(pred_scaled)[0][0]

            # Used to construct the new row that will be inserted (predicted)
            last_columns = [col for col in df_future.columns if col.startswith('Last_') and col != f'Last_{lag}']

            last_values = [df_future[col].iloc[-1] for col in last_columns] # Fill in the values

            last_trade_price = df_future['Last trade price'].iloc[-1]

            # The last one are nan because after i will fill them with te value of SMA, EMA, STD
            # Because i need the SMA, EMA, STD to make the next prediction
            new_row = [round(pred_price, 2)] + last_values + [last_trade_price, np.nan, np.nan, np.nan]

            last_date = df_future.index[-1]
            next_date = last_date + pd.Timedelta(days=1)

            df_future.loc[next_date] = new_row

            # So now i appended the new price
            # Now i calculate the technical indicators including also the newly predicted date
            sma = df_future['Last trade price'].rolling(window=14).mean()
            ema = df_future['Last trade price'].ewm(span=14, adjust=False).mean()
            std = df_future['Last trade price'].rolling(window=14).std()

            SMA = sma.iloc[-1]
            EMA = ema.iloc[-1]
            STD = std.iloc[-1]

            df_future.at[next_date, 'SMA'] = SMA
            df_future.at[next_date, 'EMA'] = EMA
            df_future.at[next_date, 'STD'] = STD

            # Store the forecast in a list
            future_predictions.loc[len(future_predictions)] = [next_date, round(pred_price, 2)]

        return future_predictions

    def _prediction_implementation(self, issuers):
        for issuer in issuers:
            data = self._pre_process(issuer)
            model = self._LSTM_MODEL(data)
            df = data.iloc[-10 - 1:].copy()
            future_prices = self._LSTM_recursive_prediction(model[0], df, model[1], model[2], 10)
            future_prices['Date'] = future_prices["Date"].dt.strftime('%m/%d/%Y')
            current_prices = data['Last trade price'].iloc[-60:].copy()
            current_prices = current_prices.reset_index()
            current_prices.rename(columns={'index': 'Date'}, inplace=True)
            current_prices['Date'] = current_prices["Date"].dt.strftime('%m/%d/%Y')
            metrics = model[4]

            self._db.save(f'{issuer}-current', 'prediction', current_prices)
            self._db.save(f'{issuer}-predicted', 'prediction', future_prices)
            self._db.save(f'{issuer}-metrics', 'prediction', metrics)

    def start(self):
        print("STARTED TRAINING THE MODELS")
        start_t = time.time()
        issuers = self._db.read('Prediction', 'prediction')['Code'].tolist()
        self._prediction_implementation(issuers)
        print('TIME TAKEN TO TRAIN AND PREDICT: ', round((time.time() - start_t) / 60, 2), 'min  or ',
              round(time.time() - start_t, 2), 'sec')
