from Repositories.Prediction_Repository import PredictionRepository


class PredictionService:
    _repository = None


    def __init__(self, issuer=None, timeframe=None):
        self._repository = PredictionRepository(issuer, timeframe)


    def get_prediction_issuers(self):
        return self._repository.get_prediction_issuers()

    def get_predicted_data(self):
        return self._repository.get_predicted_data()

    def get_current_data(self):
        return self._repository.get_current_data()

    def get_metrics(self):
        return self._repository.get_metrics()

    def get_prices(self):
        return self._repository.get_prices()

    def get_dates(self):
        return self._repository.get_dates()