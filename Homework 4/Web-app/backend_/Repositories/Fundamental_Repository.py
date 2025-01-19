
from Database.Database import Database
from Models.Fundamental_Model import FundamentalModel


class FundamentalRepository:
    def __init__(self, issuer):
        self._db = Database()
        self._issuer = issuer

    def get_fundamental_data(self):
        """Fetch the fundamental analysis data (label and score) for the given issuer."""
        # Read data from the database
        data = self._db.read(self._issuer, 'fundamental')
        if data is None or data.empty:
            return None

        # Wrap the data in the model
        model = FundamentalModel(data)
        return model.to_dict()
