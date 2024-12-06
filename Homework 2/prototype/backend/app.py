from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

FOLDER = 'C:\Users\Ardit\Desktop\Software-Design-and-Architecture\Homework 1\database'

@app.route('/api/issuers', methods=['GET'])
def get_issuers():
    df = pd.read_csv(f"{FOLDER}/Issuers.csv")
    issuers = df['Code'].tolist()
    return jsonify({'issuers': issuers})

@app.route('/api/issuer-data', methods=['POST'])
def get_issuer_data():
    issuer = request.json.get('issuer')
    if issuer:
        df = pd.read_csv(f"{FOLDER}/{issuer}.csv")
        data = df.to_dict(orient='records')

        return jsonify(data)
    return jsonify({'error': 'Issuer not found'}), 400

if __name__ == '__main__':
    app.run(debug=True)
