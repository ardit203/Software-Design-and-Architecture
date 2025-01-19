from Database.Database import Database
from Models.Prediction_Model import PredictionModel


class PredictionRepository:

    def __init__(self, issuer=None, timeframe=None):
        self._db = Database()
        if issuer is not None or timeframe is not None:
            self._issuer = issuer
            self._timeframe = timeframe
            current = self._db.read(f'{self._issuer}-current', 'prediction')
            predicted = self._db.read(f'{self._issuer}-predicted', 'prediction')
            metrics = self._db.read(f'{self._issuer}-metrics', 'prediction')
            self._model = PredictionModel(current, predicted, metrics, predicted.copy())

    def get_prediction_issuers(self):
        return self._db.read('Prediction', 'prediction')['Code'].tolist()

    def get_predicted_data(self):
        self._model.filter_by_timeframe(self._timeframe)
        return self._model.to_dict_pred()

    def get_current_data(self):
        return self._model.to_dict_current()

    def get_metrics(self):
        self._model.de_standardize_metrics()
        return self._model.to_dict_metrics()

    def get_prices(self):
        self._model.de_standardize_prices()
        return self._model.to_dict_prices()

    def get_dates(self):
        return self._model.dates()
