from Repositories.Stock_Data_Repository import StockDataRepository


class StockDataService:
    _repository = None

    def __init__(self, issuer=None, from_date=None, to_date=None):
        self._repository = StockDataRepository(issuer, from_date, to_date)

    def get_issuers(self):
        return self._repository.get_issuers()

    def get_stock_data(self):
        data = self._repository.get_stock_data()
        if not data:
            return {"error": "No stock data found."}
        return data

    def get_visual_data(self):
        data = self._repository.get_visual_data()
        if not data:
            return {"error": "No stock data found."}
        return data
