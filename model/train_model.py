import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder
import joblib

print("Libraries imported successfully!")

# Load the dataset
df = pd.read_csv("../data/medical_supply_dataset.csv")

print("Dataset loaded successfully!")
print("Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nColumn names:", list(df.columns))

# Convert medication names from text to numbers
# ML models only understand numbers, not text
le = LabelEncoder()
df["medication_encoded"] = le.fit_transform(df["medication_name"])

print("\nMedication encoding:")
for i, med in enumerate(le.classes_):
    print(f"  {med} → {i}")

# Select the input features (what the model learns from)
X = df[["medication_encoded", "current_stock", "daily_usage", "num_patients", "restocked"]]

# Select the target (what the model is trying to precdict)
y = df["days_remaining"]

print("\nInput features shape:", X.shape)
print("Target shape:", y.shape)

# Split the data into training and testing sets
# 80% for training, 20% for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\nTraining set size:", X_train.shape[0], "rows")
print("Testing set size:", X_test.shape[0], "rows")

# Train the Random Forest model
print("\nTraining the Random Forest model...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("Model trained successfully!")

# Test the model on the testing set
y_pred = model.predict(X_test)

# Calculate accuracy metrics
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nModel Accuracy Results:")
print(f"  Mean Absolute Error (MAE): {mae:.2f} days")
print(f"  R2 Score: {r2:.4f}")
print(f"  Accuracy: {r2 * 100:.2f}%")

# Show feature importance
print("\nFeature Importance:")
features = ["medication_encoded", "current_stock", "daily_usage", "num_patients", "restocked"]
for feature, importance in zip(features, model.feature_importances_):
    print(f"  {feature}: {importance * 100:.2f}%")
    
# Save the trained model
joblib.dump(model, "../model/model.pkl")

# Save the label encoder too so we can convert medication names later
joblib.dump(le, "../model/label_encoder.pkl")

print("\nModel saved as model.pkl")
print("Label encoder saved as label_encoder.pkl")
print("\nTraining complete! The model is ready to be connected to the API.")