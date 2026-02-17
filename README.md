# Rain_Prediction
Problem
Unexpected rain causes crop damage, delays, and cancellations, so a reliable day-ahead forecast helps people plan better and reduce risks. Our aim is to predict if it will rain tomorrow using historical weather data so farmers, delivery services, and event planners can avoid losses.

Significance
Unexpected rain causes crop loss, shipping delays, and cancelled events.
A reliable day-ahead prediction reduces operational risk and costs.
Practical, industry-relevant ML use case with direct business value

Dataset
Source: Public Australian weather dataset commonly distributed through the Kaggle website.<br>
Size: 145,460 daily observations (2008–2017).<br>
Features (sample): Date, Location, MinTemp, MaxTemp, Rainfall, Evaporation, Sunshine, WindGustDir, WindGustSpeed, WindDir9am, WindDir3pm, WindSpeed9am, WindSpeed3pm, Humidity9am, Humidity3pm, Pressure9am, Pressure3pm, Cloud9am, Cloud3pm, Temp9am, Temp3pm, RainToday.<br>
Label / Target: RainTomorrow (binary: Yes / No).<br>
Limitations: Missing values in some features, regional variation across locations, possible non-weather influences not captured, class imbalance (78% No, 22% Yes).

Project objectives<br>
Build and deploy a model to predict RainTomorrow with strong discrimination (AUC) and acceptable recall for rain days.<br>

Secondary objectives<br>
Compare at least two supervised models.<br>
Optimize best model and provide interpretability (SHAP).<br>
Deploy model via FastAPI and a simple Gradio/Streamlit frontend for demonstration.<br>

Evaluation metrics<br>
Primary: ROC AUC (overall ranking ability).<br>
Secondary: Precision, Recall, F1-score for the positive (rain) class; Confusion Matrix.<br>
Operational metric: Selected threshold recall/precision trade-off (e.g., prefer recall).<br>
Model selection: balance AUC and positive-class recall; prefer model with higher AUC and acceptable recall.<br>

Expected outcomes<br>
Trained model with AUC = 0.85–0.87 (baseline expectation from experiments).<br>
Final model with interpretable feature importance and SHAP explanations.<br>
Deployed API + frontend for interactive demo.<br>
Short report and slide deck summarizing methods, results, and demo.<br>

