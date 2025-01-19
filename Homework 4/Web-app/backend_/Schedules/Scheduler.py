from Scripts.Fundamental import Fundamental
from Scripts.Prediction import Prediction
from Scripts.Scrape_News import ScrapeNews
from Scripts.Scrape_Stock_Data import ScrapeStockData
from Scripts.Technical.Technical import Technical
import time


class Scheduler:
    # Is used to run four scripts that are responsible for populating the database

    _scrape_data = ScrapeStockData()
    _scrape_news = ScrapeNews()
    _tech_analysis = Technical()
    _sentiment_analysis = Fundamental()
    _train_LSTM = Prediction()


    def start(self):
        start_t = time.time()

        self._scrape_data.start()
        self._scrape_news.start()
        self._tech_analysis.start()
        self._sentiment_analysis.start()
        self._train_LSTM.start()

        print('TIME TAKEN FOR THE SCHEDULER: ', round((time.time() - start_t) / 60, 2), 'min  or ',
              round(time.time() - start_t, 2), 'sec')



