from Scripts.Standardization import Standardization


# The model for the prediction data
class PredictionModel:
    def __init__(self, current, predicted, metrics, prices):
        self._std = Standardization()
        self._current = current
        self._predicted = predicted
        self._metrics = metrics
        self._prices = prices

    def to_dict_current(self):
        """Convert the DataFrame to a list of dictionaries."""
        return self._current.to_dict(orient='records')

    def to_dict_pred(self):
        """Convert the DataFrame to a list of dictionaries."""
        return self._predicted.to_dict(orient='records')

    def to_dict_metrics(self):
        """Convert the DataFrame to a list of dictionaries."""
        return self._metrics.to_dict(orient='records')

    def to_dict_prices(self):
        """Convert the DataFrame to a list of dictionaries."""
        return self._prices.to_dict(orient='records')

    def filter_by_timeframe(self, timeframe):
        """Filter predictions based on a specific timeframe."""
        if timeframe is not None:
            timeframe = int(timeframe)
            self._predicted = self._predicted.iloc[:timeframe]
            self._prices = self._prices.iloc[:timeframe]

    def de_standardize_metrics(self):
        # It converts the numbers in to strings (formatted numbers)
        self._metrics = self._std.de_standardization(self._metrics)

    def de_standardize_prices(self):
        # It converts the numbers in to strings (formatted numbers)
        self._prices = self._std.de_standardization(self._prices)

    def dates(self):
        # Combines the dates of the current and predicted prices
        current = self._current['Date'].tolist()
        predicted = self._predicted['Date'].tolist()
        return current + predicted
