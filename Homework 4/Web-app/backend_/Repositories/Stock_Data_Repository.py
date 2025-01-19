from Database.Database import Database
from Models.Stock_Data_Model import StockDataModel


class StockDataRepository:

    def __init__(self, issuer=None, from_date=None, to_date=None):
        self._db = Database()
        if issuer is not None or from_date is not None or to_date is not None:
            self._issuer = issuer
            self._from_date = from_date
            self._to_date = to_date
            data = self._db.read(self._issuer, 'stock')
            visual = self._db.read(self._issuer, 'std')
            self._model = StockDataModel(data, visual)

    def get_issuers(self):
        return self._db.read('Issuers', 'stock')['Code'].values.tolist()

    def get_stock_data(self):
        self._model.filter_by_date_range(self._from_date, self._to_date)
        self._model.fill_missing_values()
        return self._model.to_dict(None)

    def get_visual_data(self):
        return self._model.to_dict('visual')