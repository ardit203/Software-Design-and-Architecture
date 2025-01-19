import logging
import time
import numpy as np
from transformers import pipeline
from Database.Database import Database
logging.basicConfig(level=logging.INFO)


# It is used for making the sentiment analysis for each of the issuers
class Fundamental:

    _classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    _db = Database() # This class acts like a Database, which is used for saving and reading csv files

    def _analysis(self, text_list):
            if not text_list:
                return [['NEUTRAL-NO-NEWS', 0.5]]

            scores = []
            for txt in text_list:
                chunk = txt[:512].lower()  # or do your own chunking
                try:
                    result = self._classifier(chunk)
                    scores.append(result[0]['score'])
                except Exception as e:
                    logging.error(f"Error running sentiment pipeline: {e}")

            if not scores:
                return [['NEUTRAL-NO-NEWS', 0.5]]

            avg_score = round((sum(scores) / len(scores)),2)

            sentiment = 'NEUTRAL'
            if avg_score > 0.6:
                sentiment = 'POSITIVE'
            elif avg_score < 0.4:
                sentiment = 'NEGATIVE'
            return [[sentiment, avg_score]]

    def _combine(self, issuer): # Combines the texts from all the news for an issuer
        news = self._db.read(issuer, 'news')

        if news is None:
            return []

        if news['Content'].isna().all():
            return []

        texts = news['Content'].values.tolist()

        not_nan = []
        for text in texts:
            if text is not np.nan:
                not_nan.append(text)

        return not_nan

    def _fundamental_implementation(self, issuers):
        for issuer in issuers:
            texts = self._combine(issuer)

            self._db.save(issuer, 'fundamental', self._analysis(texts))

    def start(self):
        print("STARTED THE SENTIMENT ANALYSIS")
        start_t = time.time()
        issuers = self._db.read('Issuers', 'stock')['Code'].values.tolist()
        self._fundamental_implementation(issuers)
        print('TIME TAKEN FOR SENTIMENT ANALYSIS: ', round((time.time() - start_t) / 60, 2), 'min  or ',
              round(time.time() - start_t, 2), 'sec')

