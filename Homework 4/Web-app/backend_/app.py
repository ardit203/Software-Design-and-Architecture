from flask import Flask, jsonify, request
import traceback
from flask_cors import CORS
from Schedules.Scheduler import Scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from Controllers.Fundamental_Controller import FundamentalController
from Controllers.Prediction_Controller import PredictionController
from Controllers.Stock_Data_Controller import StockDataController
from Controllers.Technical_Controller import TechnicalController

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000", }})

my_scheduler = Scheduler()

scheduler = BackgroundScheduler()

scheduler.add_job(  # Scheduler that triggers the class 'Scheduler' to run the method start()
    func=my_scheduler.start,
    trigger=CronTrigger(hour=5, minute=0),
    id="daily_task",
)


# Issuers API
@app.route('/api/issuers', methods=['GET'])
def get_issuers():
    try:
        stock_controller = StockDataController()
        issuers = stock_controller.get_issuers()
        return jsonify(issuers)
    except Exception as e:

        print(f"Error fetching issuers: {e}")
        traceback.print_exc()  # Print the full traceback to the logs
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


# Stock Data API
@app.route('/api/issuer-data', methods=['POST'])
def stock_data():
    try:
        request_data = request.json
        issuer = request_data.get('issuer')
        from_date = request_data.get('from_date')
        to_date = request_data.get('to_date')
        print(issuer, from_date, to_date)

        stock_controller = StockDataController(issuer, from_date, to_date)
        data = stock_controller.get_stock_data()
        return jsonify(data)
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Failed to fetch stock data'}), 500


# Tech analysis API
@app.route('/api/tech-analyze', methods=['POST'])
def tech_analyze():
    try:
        request_data = request.json
        issuer = request_data.get('issuer')
        indicator = request_data.get('indicator')
        from_date = request_data.get('from_date')

        tech_controller = TechnicalController(issuer, indicator, from_date)
        data = tech_controller.get_technical_data()

        return jsonify(data)
    except Exception as e:
        print(f"Error analyzing the technical indicator: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Failed to analyze the indicator'}), 500


# Fundamental analysis API
@app.route('/api/sentiment-analyze', methods=['POST'])
def sentiment_analyze():
    try:
        request_data = request.json
        issuer = request_data.get('issuer')

        fundamental_controller = FundamentalController(issuer)

        data = fundamental_controller.get_fundamental_analysis()

        return jsonify(data)
    except Exception as e:
        print(f"Error analyzing the sentiment: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Failed to analyze sentiment'}), 500


# Issuer for prediction API
@app.route('/api/prediction-issuers', methods=['GET'])
def prediction_issuers():
    try:
        prediction_controller = PredictionController()
        issuers = prediction_controller.get_prediction_issuers()
        return jsonify(issuers)
    except Exception as e:
        print(f"Error fetching issuers: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Failed to fetch issuers'}), 500


# Stock Prediction API
@app.route('/api/prediction', methods=['POST'])
def prediction():
    try:
        request_data = request.json
        issuer = request_data.get('issuer')
        timeframe = request_data.get('timeframe')
        prediction_controller = PredictionController(issuer, timeframe)
        data = prediction_controller.get_prediction_data()
        return jsonify(data)
    except Exception as e:
        print(f"Error predicting the data: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Failed to predict the data'}), 500


if __name__ == '__main__':
    print("Hello From Ardit, Sabri and Hamdi...")
    app.run(host='0.0.0.0', port=5000, debug=True)
