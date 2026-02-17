from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(title="Rain Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained sklearn XGBClassifier
try:
    model = joblib.load("rain_model.pkl")
    MODEL_FEATURES = model.feature_names_in_  # exact features model expects
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    MODEL_FEATURES = []

# Define categorical columns and their full set of possible categories
CATEGORICAL_COLUMNS = {
    'Location': [
        'Albany', 'Albury', 'AliceSprings', 'BadgerysCreek', 'Ballarat', 'Bendigo',
        'Brisbane', 'Cairns', 'Canberra', 'Cobar', 'CoffsHarbour', 'Dartmoor',
        'Darwin', 'GoldCoast', 'Hobart', 'Katherine', 'Launceston', 'Melbourne',
        'MelbourneAirport', 'Mildura', 'Moree', 'MountGambier', 'MountGinini',
        'Newcastle', 'Nhil', 'NorahHead', 'NorfolkIsland', 'Nuriootpa', 'PearceRAAF',
        'Penrith', 'Perth', 'PerthAirport', 'Portland', 'Richmond', 'Sale',
        'SalmonGums', 'Sydney', 'SydneyAirport', 'Townsville', 'Tuggeranong',
        'Uluru', 'WaggaWagga', 'Walpole', 'Watsonia', 'Williamtown', 'Witchcliffe',
        'Wollongong', 'Woomera'
    ],
    'WindGustDir': ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW'],
    'WindDir9am': ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW'],
    'WindDir3pm': ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']
}

class PredictionInput(BaseModel):
    features: dict

class PredictionOutput(BaseModel):
    prediction: int
    probability: float

def prepare_features(input_features: dict) -> pd.DataFrame:
    df = pd.DataFrame([input_features])
    
    # One-hot encode each categorical column, but only keep columns the model actually saw
    for col, cats in CATEGORICAL_COLUMNS.items():
        for cat in cats:
            dummy_col = f"{col}_{cat}"
            df[dummy_col] = 1 if df.get(col, pd.Series(['']))[0] == cat else 0
        if col in df.columns:
            df.drop(columns=col, inplace=True)
    
    # Add missing columns (set to 0) and remove extra columns
    for col in MODEL_FEATURES:
        if col not in df.columns:
            df[col] = 0
    for col in df.columns:
        if col not in MODEL_FEATURES:
            df.drop(columns=col, inplace=True)
    
    # Reorder columns exactly as model expects
    df = df[MODEL_FEATURES]
    return df

@app.get("/")
def read_root():
    return {
        "message": "Rain Prediction API",
        "status": "Model loaded" if model else "Model not loaded",
        "features_required": list(MODEL_FEATURES)
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: PredictionInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    try:
        df = prepare_features(input_data.features)
        pred_prob = model.predict_proba(df)[:,1][0]
        pred_class = int(round(pred_prob))
        return PredictionOutput(prediction=pred_class, probability=float(pred_prob))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)