import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set a seed so the random numbers are consistent every time we run this
np.random.seed(42)
random.seed(42)

# Define our 3 medications and their realistic properties
medications = {
    "Paracetamol 500mg": {
        "base_daily_usage": 24,
        "initial_stock": 500,
        "restock_amount": 400
    },
    "Amoxicillin 250mg": {
        "base_daily_usage": 18,
        "initial_stock": 300,
        "restock_amount": 250
    },
    "Ibuprofen 400mg": {
        "base_daily_usage": 22,
        "initial_stock": 450,
        "restock_amount": 350
    }
}

print("Medications defined successfully!")
print("Generating dataset...")

# Generate 365 days worth of data (1 year)
start_date = datetime(2025, 1, 1)
rows = []

for med_name, props in medications.items():
    current_stock = props["initial_stock"]
    
    for day in range(365):
        # Calculate the current date
        current_date = start_date + timedelta(days=day)
        
        # Add some randomness to daily usage to make it realistic
        # Some days more patients, some days fewer
        daily_usage = int(props["base_daily_usage"] * random.uniform(0.7, 1.3))
        
        # Number of patients is related to usage
        num_patients = int(daily_usage * random.uniform(0.8, 1.2))
        
        # Deduct usage from stock
        current_stock -= daily_usage
        
        # Restock when stock gets low
        restocked = 0
        if current_stock < 50:
            current_stock += props["restock_amount"]
            restocked = props["restock_amount"]
        
        # Calculate days remaining
        days_remaining = current_stock / props["base_daily_usage"]
        
        # Save this row
        rows.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "medication_name": med_name,
            "current_stock": current_stock,
            "daily_usage": daily_usage,
            "num_patients": num_patients,
            "restocked": restocked,
            "days_remaining": round(days_remaining)
        })

print(f"Generated {len(rows)} rows of data!")

# Convert the rows into a pandas DataFrame
df = pd.DataFrame(rows)

# Save the dataset as a CSV file
df.to_csv("medical_supply_dataset.csv", index=False)

print("Dataset saved as medical_supply_dataset.csv!")
print("\nFirst 5 rows of the dataset:")
print(df.head())
print("\nDataset shape:", df.shape)
print("\nDataset columns:", list(df.columns))