from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import joblib
import numpy as np
import os

# Load the trained model and label encoder
model = joblib.load("../model/model.pkl")
le = joblib.load("../model/label_encoder.pkl")

print("ML Model loaded successfully!")

# Create the Flask app
app = Flask(__name__)
CORS(app)

# medication data
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

# Function that predicts using the trained Random Forest model
def predict_depletion(medication_name, current_stock, daily_usage, num_patients=5, restocked=0):
    
    # Convert medication name to a number using the label encoder
    medication_encoded = le.transform([medication_name])[0]
    
    # Prepare the input data for the model
    input_data = np.array([[medication_encoded, current_stock, daily_usage, num_patients, restocked]])
    
    # Use the trained model to predict days remaining
    days_remaining = model.predict(input_data)[0]
    
    # Calculate the depletion date
    depletion_date = datetime.now() + timedelta(days=days_remaining)
    
    # Determine status based on days remaining
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
        prediction = predict_depletion(name, data["current_stock"], data["daily_usage"])
        
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

    prediction = predict_depletion(name, current_stock, daily_usage)

    return jsonify({
        "name": name,
        "current_stock": current_stock,
        "daily_usage": daily_usage,
        "days_remaining": prediction["days_remaining"],
        "depletion_date": prediction["depletion_date"],
        "status": prediction["status"]
    })

# Store nurse submissions (acts as a simple database for now)
submissions = []

# Endpoint 4: Save a nurse's medication usage submission
@app.route('/submit-usage', methods=['POST'])
def submit_usage():
    data = request.get_json()

    name = data.get("medication_name")
    quantity = data.get("quantity")
    patients = data.get("patients")
    date = data.get("date")

    # Validate the data
    if not name or not quantity or not patients or not date:
        return jsonify({"error": "Please provide all fields"}), 400

    # Save the submission
    submission = {
        "medication_name": name,
        "quantity": quantity,
        "patients": patients,
        "date": date
    }
    submissions.append(submission)

    # Update the medication stock
    if name in medications:
        medications[name]["current_stock"] -= int(quantity)
        if medications[name]["current_stock"] < 0:
            medications[name]["current_stock"] = 0

    return jsonify({
        "message": "Usage recorded successfully!",
        "submission": submission
    })


# Endpoint 5: Get all nurse submissions
@app.route('/submissions', methods=['GET'])
def get_submissions():
    return jsonify(submissions)

# Endpoint 6: Update stock level for a medication
@app.route('/update-stock', methods=['POST'])
def update_stock():
    data = request.get_json()
    
    name = data.get("medication_name")
    new_stock = data.get("new_stock")
    
    # Validate the data
    if not name or new_stock is None:
        return jsonify({"error": "Please provide medication name and new stock"}), 400
    
    # Check if medication exists
    if name not in medications:
        return jsonify({"error": "Medication not found"}), 404
    
    # Update the stock
    medications[name]["current_stock"] = int(new_stock)
    
    return jsonify({
        "message": f"Stock for {name} updated successfully!",
        "medication": name,
        "new_stock": int(new_stock)
    })

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)