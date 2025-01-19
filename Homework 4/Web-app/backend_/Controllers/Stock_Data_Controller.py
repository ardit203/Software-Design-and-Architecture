from Services.Stock_Data_Service import StockDataService

class StockDataController:
    _service = None

    def __init__(self, issuer=None, from_date=None, to_date=None):
        self._service = StockDataService(issuer, from_date, to_date)


    def get_issuers(self):
        return self._service.get_issuers()

    def get_stock_data(self):

        stock = self._service.get_stock_data()
        visual = self._service.get_visual_data()

        return [
            stock,
            visual
        ]