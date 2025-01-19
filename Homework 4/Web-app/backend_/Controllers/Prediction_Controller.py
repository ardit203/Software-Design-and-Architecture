
from Services.Prediction_Service import PredictionService


class PredictionController:
    _service = None

    def __init__(self, issuer=None, timeframe=None):
        self._service = PredictionService(issuer, timeframe)

    def get_prediction_issuers(self):
        return self._service.get_prediction_issuers()

    def get_prediction_data(self):
        """Return predicted data."""
        predicted = self._service.get_predicted_data()
        current = self._service.get_current_data()
        metrics = self._service.get_metrics()
        prices = self._service.get_prices()
        dates = self._service.get_dates()

        return [
            current,
            predicted,
            metrics,
            dates,
            prices
        ]
