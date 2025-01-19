from Database.Database import Database
from Models.Technical_Model import TechnicalModel



class TechnicalRepository:
    def __init__(self, issuer, indicator, from_date=None):
        self._db = Database()
        self._issuer = issuer
        self._indicator = indicator
        self._from_date = from_date

    def get_technical_data(self):
        """Fetch and process technical data."""
        # Fetch raw data from the database
        data = self._db.read(self._issuer, 'technical')
        if data is None:
            return None

        # Create a TechnicalModel instance
        model = TechnicalModel(data)

        # Filter and transform the data
        model.filter_by_date(self._from_date)
        model.prepare_for_analysis(self._indicator)

        return model.to_dict()

