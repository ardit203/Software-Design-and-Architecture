from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

FOLDER = 'D:/Faculty/5th Semester/PYTHON/Homework1/database'

@app.route('/api/issuers', methods=['GET'])
def get_issuers():
    # Load the Excel file and read the issuers from it
    df = pd.read_excel(f"{FOLDER}/issuers.xlsx")
    issuers = df['Code'].tolist()  # Assuming column is 'issuer_name'
    print(issuers)
    return jsonify({'issuers': issuers})

@app.route('/api/issuer-data', methods=['POST'])
def get_issuer_data():
    issuer = request.json.get('issuer')
    if issuer:
        # Load data for the selected issuer
        df = pd.read_excel(f"{FOLDER}/{issuer}.xlsx")
        df = df.iloc[:100]
        data = df.to_dict(orient='records')

        return jsonify(data)
    return jsonify({'error': 'Issuer not found'}), 400

if __name__ == '__main__':
    app.run(debug=True)
