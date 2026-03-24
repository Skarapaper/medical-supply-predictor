from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta

# Create the Flask app
app = Flask(__name__)
CORS(app)

# Simulated medication data
medications = {
    "Paracetamol 500mg": {
        "current_stock": 120,
        "daily_usage": 24,
        "department": "Emergency"
    },
    "Amoxicillin 250mg": {
        "current_stock": 35,
        "daily_usage": 18,
        "department": "ICU"
    },
    "Ibuprofen 400mg": {
        "current_stock": 280,
        "daily_usage": 22,
        "department": "Surgery"
    }
}

# Function that predicts when a medication will run out
def predict_depletion(current_stock, daily_usage):
    days_remaining = current_stock / daily_usage
    depletion_date = datetime.now() + timedelta(days=days_remaining)

    if days_remaining <= 5:
        status = "Critical"
    elif days_remaining <= 14:
        status = "Low"
    else:
        status = "Normal"

    return {
        "days_remaining": round(days_remaining),
        "depletion_date": depletion_date.strftime("%Y-%m-%d"),
        "status": status
    }

# Endpoint 1: Check if the API is running
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "API is running",
        "message": "MedSupply AI backend is active"
    })

# Endpoint 2: Get all medications with their predictions
@app.route('/medications', methods=['GET'])
def get_medications():
    results = []

    for name, data in medications.items():
        prediction = predict_depletion(data["current_stock"], data["daily_usage"])

        results.append({
            "name": name,
            "current_stock": data["current_stock"],
            "daily_usage": data["daily_usage"],
            "department": data["department"],
            "days_remaining": prediction["days_remaining"],
            "depletion_date": prediction["depletion_date"],
            "status": prediction["status"]
        })

    return jsonify(results)

# Endpoint 3: Predict depletion for a specific medication
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    name = data.get("name")
    current_stock = data.get("current_stock")
    daily_usage = data.get("daily_usage")

    if not name or not current_stock or not daily_usage:
        return jsonify({"error": "Please provide name, current_stock and daily_usage"}), 400

    prediction = predict_depletion(current_stock, daily_usage)

    return jsonify({
        "name": name,
        "current_stock": current_stock,
        "daily_usage": daily_usage,
        "days_remaining": prediction["days_remaining"],
        "depletion_date": prediction["depletion_date"],
        "status": prediction["status"]
    })

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)