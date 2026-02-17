import joblib
import xgboost as xgb

# Load your old pickle model
model = joblib.load("rain_model.pkl")

# Save it in XGBoost's native format
model.save_model("rain_model.json")