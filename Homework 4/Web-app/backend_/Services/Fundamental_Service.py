from Repositories.Fundamental_Repository import FundamentalRepository

class FundamentalService:
    def __init__(self, issuer):
        self._repository = FundamentalRepository(issuer)

    def get_fundamental_data(self):
        """Retrieve fundamental data as a dictionary."""
        data = self._repository.get_fundamental_data()
        if not data:
            return {"error": "No fundamental data found."}
        return data
