import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from keras import Sequential, Input
from keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.preprocessing import MinMaxScaler
from backend.scripts.other.standardization import to_numbers, dates, standardization
import numpy as np
from datetime import datetime, timedelta

FOLDER = 'D:/Faculty/5th Semester/PYTHON/backend/database'

def pre_process(issuer):
    data = pd.read_csv(f'{FOLDER}/{issuer}.csv')
    df = data[['Date', 'Last trade price']].copy()
    df = standardization(df)
    df.set_index('Date', inplace=True)
    lag = 5
    periods = range(lag, 0, -1)

    for period in periods:
        df[f'Last_{period}'] = df['Last trade price'].shift(period)

    df.dropna(inplace=True)
    return df


def LSTM_MODEL(data):
    X, Y = data.drop(columns=['Last trade price']), data['Last trade price']

    train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.3, shuffle=False)

    scaler_X = MinMaxScaler()
    train_X = scaler_X.fit_transform(train_X)
    test_X = scaler_X.transform(test_X)

    scaler_Y = MinMaxScaler()
    train_Y = scaler_Y.fit_transform(train_Y.to_numpy().reshape(-1, 1))

    train_X = train_X.reshape(train_X.shape[0], 5, (train_X.shape[1] // 5))  # (samples, timesteps, features)
    test_X = test_X.reshape(test_X.shape[0], 5, (test_X.shape[1] // 5))

    model = Sequential([
        Input((train_X.shape[1], train_X.shape[2],)),
        # LSTM(32, activation="relu", return_sequences=True),
        # Dropout(0.2),
        LSTM(32, activation="relu"),
        Dense(1, activation="linear")
    ])

    model.summary()

    model.compile(
        loss="mean_squared_error",
        optimizer="adam",
        metrics=["mean_squared_error"],
    )

    history = model.fit(train_X, train_Y, validation_split=0.3, epochs=16, batch_size=16, shuffle=False)

    # sns.lineplot(history.history["loss"], label="loss")
    # sns.lineplot(history.history["val_loss"], label="val_loss")
    # plt.show()

    pred_Y = model.predict(test_X)

    pred_Y = scaler_Y.inverse_transform(pred_Y)
    metrics = {'r2_score': round(r2_score(test_Y, pred_Y),2),
               'MSE': round(mean_squared_error(test_Y, pred_Y),2),
               'MAE': round(mean_absolute_error(test_Y, pred_Y),2)}
    print(metrics)

    return [model, scaler_X, scaler_Y, data, metrics]


def LSTM_Prediction(model, df, scaler_X, scaler_Y, n_days):

    future_predictions = pd.DataFrame(columns=['Date', 'Last trade price'])

    for i in range(0, n_days):
        scaled = scaler_X.transform(df[-1:].drop(columns=['Last trade price']))
        scaled = scaled.reshape(scaled.shape[0], 5, (scaled.shape[1] // 5))
        tomorrow = model.predict(scaled)
        tomorrow = scaler_Y.inverse_transform(tomorrow)



        last_date = df.index[-1]
        next_date = last_date + pd.Timedelta(days=1)

        price = float(tomorrow[0][0])
        df.loc[next_date] = [round(price, 2), df['Last_4'].iloc[-1], df['Last_3'].iloc[-1],
                             df['Last_2'].iloc[-1], df['Last_1'].iloc[-1], df['Last trade price'].iloc[-1]]
        future_predictions.loc[len(future_predictions)] = [next_date, round(price, 2)]

    return future_predictions


def lstm_main(issuer, timeframe):
    data = pre_process(issuer)
    model = LSTM_MODEL(data)
    data = model[3]
    df = data.iloc[-timeframe-1:].copy()


    future_prices = LSTM_Prediction(model[0], df, model[1], model[2], timeframe)
    future_prices['Date'] = future_prices["Date"].dt.strftime('%m/%d/%Y')
    current_prices = data['Last trade price'].iloc[-60:].copy()
    current_prices = current_prices.reset_index()
    current_prices.rename(columns={'index': 'Date'}, inplace=True)
    current_prices['Date'] = current_prices["Date"].dt.strftime('%m/%d/%Y')
    metrics = pd.DataFrame([model[4]])

    return [current_prices, future_prices, metrics]




if __name__ == '__main__':
    lstm_main('KMB', 5)
