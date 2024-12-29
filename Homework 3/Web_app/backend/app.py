from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from backend.scripts.other.scraper import main as scraper_main
from backend.scripts.other.standardization import visual_standardization
from backend.scripts.other.table_generator import create_table
from backend.scripts.analysis.technical import tech_main
from backend.scripts.analysis.fundamental import fundamental_main
from backend.scripts.analysis.lstm import lstm_main

app = Flask(__name__)
CORS(app)

FOLDER = 'D:/Faculty/5th Semester/PYTHON/backend/database'


############ Scraper ######  /api/fetch-new-data   ######################################
@app.route('/api/fetch-new-data', methods=['POST'])
def fetch_new_data():
    try:
        scraper_main()
        return jsonify({'message': 'New data fetched and saved successfully!'}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to fetch new data'}), 500


################## Issuers ######## /api/issuers ########################################
@app.route('/api/issuers', methods=['GET'])
def get_issuers():
    try:
        df = pd.read_csv(f"{FOLDER}/Issuers.csv")
        issuers = df['Code'].tolist()
        return jsonify(issuers)
    except Exception as e:
        print(f"Error fetching issuers: {e}")
        return jsonify({'error': 'Failed to fetch issuers'}), 500


############ Issuer Table  #### api/issuer-data ##################################
@app.route('/api/issuer-data', methods=['POST'])
def get_issuer_data():
    request_data = request.json
    issuer = request_data.get('issuer')
    from_date = request_data.get('from_date')
    to_date = request_data.get('to_date')
    df = create_table(issuer, from_date, to_date)
    std = visual_standardization(df)
    data = [df.to_dict(orient='records'), std.to_dict(orient='records')]
    return jsonify(data)


############## Tech-analysis #### api/tech-analyze ##################
@app.route('/api/tech-analyze', methods=['POST'])
def analyze():
    request_data = request.json
    issuer = request_data.get('issuer')
    indicator = request_data.get('indicator')
    from_date = request_data.get('from_date')

    data = tech_main(issuer, indicator, from_date)
    data.fillna('', inplace=True)
    df = data.to_dict(orient='records')
    return jsonify(df)


############# Sentiment-analysis ## api/sentiment-analyze ####################
@app.route('/api/sentiment-analyze', methods=['POST'])
def sentiment():
    # Extract request data
    request_data = request.json
    issuer = request_data.get('issuer')

    # Debug print to verify data
    print("Issuer:", issuer)


    sentiment_result = fundamental_main(issuer)


    # Return the result as JSON
    return jsonify(sentiment_result)


######## Issuers for Prediction ## api/prediction-issuers
@app.route('/api/prediction-issuers', methods=['GET'])
def prediction_issuers():
    try:
        df = pd.read_csv(f"{FOLDER}/Issuers-Prediction.csv")
        issuers = df['Code'].tolist()
        return jsonify(issuers)
    except Exception as e:
        print(f"Error fetching issuers: {e}")
        return jsonify({'error': 'Failed to fetch issuers'}), 500





######## Stock Prediction ## api/prediction
@app.route('/api/prediction', methods=['POST'])
def prediction():
    request_data = request.json
    issuer = request_data.get('issuer')
    timeframe = int(request_data.get('timeframe'))



    data = lstm_main(issuer, timeframe)

    current = data[0].to_dict(orient='records')
    future = data[1].to_dict(orient='records')
    metrics = data[2].to_dict(orient='records')
    current_dates = [record['Date'] for record in current]
    future_dates = [record['Date'] for record in future]
    merged_dates = current_dates + future_dates
    print(metrics)
    return jsonify([ current, future, metrics,  merged_dates])

if __name__ == '__main__':
    app.run(debug=True)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
