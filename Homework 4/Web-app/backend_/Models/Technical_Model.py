from datetime import datetime
import pandas as pd

# Technical Data Model
class TechnicalModel:
    def __init__(self, data):
        self._data = data

    def to_dict(self):
        """Convert the data to a dictionary format."""
        return self._data.to_dict(orient='records')

    def filter_by_date(self, from_date=None):
        """Filter data based on a starting date."""
        if from_date:
            from_date = datetime.strptime(from_date, '%Y-%m-%d')
            self._data['Date'] = pd.to_datetime(self._data['Date'])
            self._data = self._data[self._data['Date'] >= from_date]
            self._data['Date'] = self._data['Date'].dt.strftime('%m/%d/%Y')  # Reformat date

    def prepare_for_analysis(self, indicator):
        """Prepare data for technical analysis by selecting relevant columns."""
        columns = [
            'Date',
            f'1 Day {indicator}', f'1 Week {indicator}', f'1 Month {indicator}',
            f'1 Day {indicator} Signals', f'1 Week {indicator} Signals', f'1 Month {indicator} Signals'
        ]
        self._data = self._data[columns].fillna('')