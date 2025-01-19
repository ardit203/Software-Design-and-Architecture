
class FundamentalModel:
    def __init__(self, data):
        self._data = data

    def to_dict(self):
        """Convert the DataFrame to a list of dictionaries."""
        return self._data.to_dict(orient='records')
