from datetime import datetime
import pandas as pd

# The stock data model
class StockDataModel:

    def __init__(self, data, visual):
        self._data = data
        self._visual = visual

    def to_dict(self, type):
        """Convert data to a dictionary format."""
        if type == 'visual':
            return self._visual.to_dict(orient='records')
        else:
            return self._data.to_dict(orient='records')

    def filter_by_date_range(self, from_date=None, to_date=None):
        """Filter data by date range."""
        if from_date:
            from_date = datetime.strptime(from_date, '%Y-%m-%d')
            self._data['Date'] = pd.to_datetime(self._data['Date'])
            self._data = self._data[self._data['Date'] >= from_date]
            self._visual['Date'] = pd.to_datetime(self._visual['Date'])
            self._visual = self._visual[self._visual['Date'] >= from_date]

        if to_date:
            to_date = datetime.strptime(to_date, '%Y-%m-%d')
            self._data = self._data[self._data['Date'] <= to_date]
            self._visual = self._visual[self._visual['Date'] <= to_date]
            self._data['Date'] = self._data['Date'].dt.strftime('%m/%d/%Y')
            self._visual['Date'] = self._visual['Date'].dt.strftime('%m/%d/%Y')

    def fill_missing_values(self):
        """Fill missing values with appropriate defaults."""
        self._data.fillna('', inplace=True)
        self._visual['Max'] = self._visual['Max'].fillna(self._visual['Last trade price'])
        self._visual['Min'] = self._visual['Min'].fillna(self._visual['Last trade price'])

    def get_numerical_data(self):
        """Prepare data for numerical table display."""
        return self._data

    def get_visualization_data(self):
        # Data that is used for the visualization
        return self._visual
