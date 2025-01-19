from Repositories.Technical_Repository import TechnicalRepository


class TechnicalService():
    _repository = None

    def __init__(self, issuer, indicator, from_date=None):
        self._repository = TechnicalRepository(issuer, indicator, from_date)

    def get_technical_data(self):
        data = self._repository.get_technical_data()
        if not data:
            return {"error": "No technical data found."}
        return data
