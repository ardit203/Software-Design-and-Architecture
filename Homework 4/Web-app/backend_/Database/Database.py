import os
import pandas as pd
import threading
from Scripts.Standardization import Standardization

DATA_PATH = os.getenv("DATA_PATH", "/app/backend_/Database/data")  # Env data path

STOCK_COLUMNS = ["Date", "Last trade price", "Max", "Min", "Avg.Price", "%chg.", "Volume",
                 "Turnover in BEST in denars", "Total turnover in denars"]

ISSUERS_COLUMNS = ['Code']

LAST_DATES_COLUMNS = ['Code', 'Date']

NEWS_COLUMNS = ['Date', 'Link', 'Content']


# Used for reading and writing in to csv file
# Manages all the work with files

class Database:
    instance = None
    lock = threading.Lock()
    _path = None
    _std = Standardization()

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            with cls.lock:
                if not cls.instance:
                    cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    @classmethod
    def set_path(cls, filename, type):
        """Set the class-level _path variable."""
        cls._path = os.path.join(DATA_PATH, f"{filename}-{type}.csv")

    @classmethod
    def get_path(cls):
        """Get the current value of the class-level _path variable."""
        return cls._path

    def _save_stock(self, filename, new_data):
        if filename == 'Issuers':
            pd.DataFrame(new_data, columns=ISSUERS_COLUMNS).to_csv(self.get_path(), index=False)
            return
        elif filename == 'LastDates':
            pd.DataFrame(new_data, columns=LAST_DATES_COLUMNS).to_csv(self.get_path(), index=False)
            return
        elif os.path.exists(self.get_path()):
            existing = pd.read_csv(self.get_path())
            new_data = pd.DataFrame(new_data, columns=STOCK_COLUMNS)
            data = pd.concat([new_data, existing], axis=0)
            data.to_csv(self.get_path(), index=False)
            print(f"Appended data for {filename}")
        else:
            pd.DataFrame(new_data, columns=STOCK_COLUMNS).to_csv(self.get_path(), index=False)
            print(f'Saved data for {filename}')

    def _read_stock(self):
        if self._exists_stock():
            return pd.read_csv(self.get_path())
        return None

    def _exists_stock(self):
        return os.path.exists(self.get_path())

    def _save_news(self, data):
        pd.DataFrame(data, columns=NEWS_COLUMNS).to_csv(
            self.get_path(), index=False)

    def _read_news(self):
        if os.path.exists(self.get_path()):
            return pd.read_csv(self.get_path())

        return None

    def _exists_news(self):
        return os.path.exists(self.get_path())

    def _save_pred(self, filename, data):
        data.to_csv(self.get_path(), index=False)
        print(f"Saved prediction data for {filename}")

    def _read_pred(self):
        if os.path.exists(self.get_path()):
            return pd.read_csv(self.get_path())

        return None

    def _save_fundamental(self, filename, data):
        pd.DataFrame(data, columns=['Label', 'Score']).to_csv(self.get_path(), index=False)
        print(f"Saved fundamental data for {filename}")

    def _read_fundamental(self):
        if os.path.exists(self.get_path()):
            return pd.read_csv(self.get_path())

        return None

    def _save_tech(self, filename, data):
        data.to_csv(self.get_path(), index=False)
        print(f"Saved tech data for {filename}")

    def _read_tech(self):
        if os.path.exists(self.get_path()):
            return pd.read_csv(self.get_path())

        return None

    def _save_std(self, filename, data):
        new_data = pd.DataFrame(data, columns=STOCK_COLUMNS)
        new_data = self._std.standardization(new_data)

        if os.path.exists(self.get_path()):
            existing = pd.read_csv(self.get_path())
            data = pd.concat([existing, new_data], axis=0)
            data.to_csv(self.get_path(), index=False)
            print(f"Appended std data for {filename}")
        else:
            new_data.to_csv(self.get_path(), index=False)
            print(f'Saved std data for {filename}')

    def _read_std(self):
        if os.path.exists(self.get_path()):
            return pd.read_csv(self.get_path())
        return None

    def save(self, filename, type, data):
        self.set_path(filename, type)
        if type == 'stock':
            self._save_stock(filename, data)
        elif type == 'news':
            self._save_news(data)
        elif type == 'prediction':
            self._save_pred(filename, data)
        elif type == 'fundamental':
            self._save_fundamental(filename, data)
        elif type == 'technical':
            self._save_tech(filename, data)
        elif type == 'std':
            self._save_std(filename, data)

    def read(self, filename, type):
        self.set_path(filename, type)
        if type == 'stock':
            return self._read_stock()
        elif type == 'news':
            return self._read_news()
        elif type == 'prediction':
            return self._read_pred()
        elif type == 'fundamental':
            return self._read_fundamental()
        elif type == 'technical':
            return self._read_tech()
        elif type == 'std':
            return self._read_std()

        return

    def exists(self, filename, type):
        self.set_path(filename, type)
        if type == 'stock':
            return self._exists_stock()
        elif type == 'news':
            return self._exists_news()
