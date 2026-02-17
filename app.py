import streamlit as st
import requests
import json

# --- Configuration ---
API_URL = "http://localhost:8000"

# --- Dark Theme Visual Settings ---
DARK_PRIMARY_BG = "#1e212b"    # Deep dark gray/blue
DARK_SECONDARY_BG = "#2c303a"  # Slightly lighter dark gray/blue for containers
TEXT_COLOR = "#f0f2f6"         # Light gray/off-white text

# Accent Colors
RAIN_COLOR = "#4a90e2"         # Soft Blue for Rain/Success
SUN_COLOR = "#f5a623"          # Amber/Orange for No Rain/Warning
BUTTON_COLOR = "#007bff"       # Standard Streamlit Blue

st.set_page_config(
    page_title="Rain Prediction App",
    page_icon="💧",
    layout="wide"
)

# --- Dark Theme Custom CSS ---
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {DARK_PRIMARY_BG};
        color: {TEXT_COLOR};
    }}
    [data-testid="stSidebar"] {{
        background-color: {DARK_SECONDARY_BG};
    }}
    .st-emotion-cache-1kyy532 {{
        background-color: {DARK_SECONDARY_BG} !important;
    }}
    h1, h2, h3, h4, p, label {{
        color: {TEXT_COLOR} !important;
    }}
    .st-emotion-cache-13mo5u9, .st-emotion-cache-1cpx9i5, .st-emotion-cache-nahz7x {{
        background-color: {DARK_SECONDARY_BG} !important;
        border: 1px solid #444;
        color: {TEXT_COLOR} !important;
    }}
    [data-testid="stAlert"] > div[style*="background-color: rgb(18, 201, 127)"] {{
        background-color: {RAIN_COLOR} !important;
        color: {DARK_PRIMARY_BG};
        border-left: 8px solid #0056b3;
    }}
    [data-testid="stAlert"] > div[style*="background-color: rgb(240, 242, 246)"] {{
        background-color: {SUN_COLOR} !important;
        color: {DARK_PRIMARY_BG};
        border-left: 8px solid #d39e00;
    }}
    [data-testid="stMetric"] {{
        background-color: {DARK_SECONDARY_BG};
        color: {TEXT_COLOR};
        border: 1px solid #444;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }}
    [data-testid="stExpander"] {{
        background-color: {DARK_SECONDARY_BG};
        border-radius: 8px;
        padding: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Main Title ---
st.title("💧 Rain Prediction AI ☀️")
st.markdown(
    '<p style="text-align: center; font-size: 1.2rem; color: #aaa;">'
    '**Predicting tomorrow\'s weather with Machine Learning.**</p>',
    unsafe_allow_html=True
)
st.divider()

# --- API Status ---
with st.expander("🌐 API & Model Status", expanded=True):
    api_col, model_col = st.columns(2)
    try:
        health = requests.get(f"{API_URL}/health", timeout=2)
        if health.status_code == 200:
            api_col.success("✅ API Connected")
            if health.json().get("model_loaded"):
                model_col.success("🧠 Model Loaded")
            else:
                model_col.warning("⚠️ Model Not Loaded (Check Backend)")
        else:
            api_col.error("❌ API Error")
            model_col.error("❌ Model Check Failed")
    except:
        api_col.error("❌ Cannot connect to API")
        model_col.error("❌ Model Check Failed")

st.divider()

# --- Feature Inputs ---
st.header("1. Input Weather Conditions")
tab1, tab2, tab3, tab4 = st.tabs(
    ["🌡️ Temperature & Rain", "🌬️ Wind", "☁️ Atmospheric", "📍 Location & Rain Today"]
)

# Tab 1: Temperature & Rain
with tab1:
    st.subheader("Temperature & Rainfall Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        MinTemp = st.number_input("Minimum Temperature (°C)", value=13.0, step=0.1, format="%.1f")
        MaxTemp = st.number_input("Maximum Temperature (°C)", value=23.0, step=0.1, format="%.1f")
    with col2:
        Rainfall = st.number_input("Rainfall Today (mm)", value=0.0, step=0.1, min_value=0.0, format="%.1f")
        Evaporation = st.number_input("Evaporation (mm)", value=5.0, step=0.1, min_value=0.0, format="%.1f")
    with col3:
        Sunshine = st.number_input("Sunshine (hours)", value=8.0, step=0.1, min_value=0.0, max_value=24.0, format="%.1f")
        Temp9am = st.number_input("Temperature at 9 AM (°C)", value=17.0, step=0.1, format="%.1f")
        Temp3pm = st.number_input("Temperature at 3 PM (°C)", value=22.0, step=0.1, format="%.1f")

# Tab 2: Wind
wind_dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
with tab2:
    st.subheader("Wind Speed and Direction")
    col1, col2, col3 = st.columns(3)
    with col1:
        WindGustDir = st.selectbox("Wind Gust Direction", wind_dirs)
        WindGustSpeed = st.number_input("Wind Gust Speed (km/h)", value=35.0, step=1.0, min_value=0.0)
    with col2:
        WindDir9am = st.selectbox("Wind Direction at 9 AM", wind_dirs)
        WindSpeed9am = st.number_input("Wind Speed at 9 AM (km/h)", value=15.0, step=1.0, min_value=0.0)
    with col3:
        WindDir3pm = st.selectbox("Wind Direction at 3 PM", wind_dirs)
        WindSpeed3pm = st.number_input("Wind Speed at 3 PM (km/h)", value=20.0, step=1.0, min_value=0.0)

# Tab 3: Atmospheric
with tab3:
    st.subheader("Pressure, Humidity, and Cloud Cover")
    col1, col2 = st.columns(2)
    with col1:
        Humidity9am = st.slider("Humidity at 9 AM (%)", 0, 100, 70)
        Humidity3pm = st.slider("Humidity at 3 PM (%)", 0, 100, 50)
        Pressure9am = st.number_input("Pressure at 9 AM (hPa)", value=1013.0, step=0.1)
    with col2:
        Pressure3pm = st.number_input("Pressure at 3 PM (hPa)", value=1012.0, step=0.1)
        Cloud9am = st.slider("Cloud Cover at 9 AM (oktas)", 0, 8, 4)
        Cloud3pm = st.slider("Cloud Cover at 3 PM (oktas)", 0, 8, 5)

# Tab 4: Location & Rain Today
locations = [
    "Albany", "Albury", "AliceSprings", "BadgerysCreek", "Ballarat", "Bendigo", "Brisbane",
    "Cairns", "Canberra", "Cobar", "CoffsHarbour", "Dartmoor", "Darwin", "GoldCoast",
    "Hobart", "Katherine", "Launceston", "Melbourne", "MelbourneAirport", "Mildura",
    "Moree", "MountGambier", "MountGinini", "Newcastle", "Nhil", "NorahHead",
    "NorfolkIsland", "Nuriootpa", "PearceRAAF", "Penrith", "Perth", "PerthAirport",
    "Portland", "Richmond", "Sale", "SalmonGums", "Sydney", "SydneyAirport",
    "Townsville", "Tuggeranong", "Uluru", "WaggaWagga", "Walpole", "Watsonia",
    "Williamtown", "Witchcliffe", "Wollongong", "Woomera"
]
with tab4:
    st.subheader("Location and Historical Data")
    col1, col2 = st.columns(2)
    with col1:
        Location = st.selectbox("Weather Station Location", locations, index=locations.index("Sydney"))
    with col2:
        RainToday = st.radio("Was there Rain Today?", ["No", "Yes"], index=0, horizontal=True)

# Collect features
features = {
    "MinTemp": MinTemp, "MaxTemp": MaxTemp, "Rainfall": Rainfall, "Evaporation": Evaporation,
    "Sunshine": Sunshine, "WindGustSpeed": WindGustSpeed, "WindSpeed9am": WindSpeed9am,
    "WindSpeed3pm": WindSpeed3pm, "Humidity9am": Humidity9am, "Humidity3pm": Humidity3pm,
    "Pressure9am": Pressure9am, "Pressure3pm": Pressure3pm, "Cloud9am": Cloud9am,
    "Cloud3pm": Cloud3pm, "Temp9am": Temp9am, "Temp3pm": Temp3pm,
    "RainToday": 1 if RainToday == "Yes" else 0,
    "Location": Location, "WindGustDir": WindGustDir, "WindDir9am": WindDir9am,
    "WindDir3pm": WindDir3pm
}

st.divider()

# --- Prediction Button & Result ---
st.header("2. Prediction")
result_container = st.container()

if st.button("🔮 **PREDICT TOMORROW'S RAIN**", type="primary", use_container_width=True):
    with st.spinner("Analyzing atmospheric data..."):
        try:
            response = requests.post(f"{API_URL}/predict", json={"features": features}, timeout=5)
            with result_container:
                if response.status_code == 200:
                    result = response.json()
                    prediction = result["prediction"]
                    probability = result["probability"]
                    st.markdown("### 📣 Prediction Results")
                    if prediction == 1:
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.image("https://media.giphy.com/media/l4pTcQ4GbpYlH1Q6c/giphy.gif")
                        with col2:
                            st.success(f"## 🌧️ YES: Rain Expected Tomorrow")
                            st.metric("Rain Probability", f"{probability*100:.2f}%")
                            st.markdown("**Recommendation:** Best to pack an umbrella!")
                    else:
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.image("https://media.giphy.com/media/3o7TKBH7T8q6k5B2k8/giphy.gif")
                        with col2:
                            st.info(f"## ☀️ NO: No Rain Expected Tomorrow")
                            st.metric("Clear Sky Confidence", f"{(1-probability)*100:.2f}%")
                            st.markdown("**Recommendation:** Enjoy the good weather!")
                    with st.expander("🔎 View Raw Model Input Data"):
                        st.json(features)
                else:
                    st.error(f"Prediction failed: {response.status_code} - {response.text}")
        except requests.exceptions.Timeout:
            st.error("Request timed out. Ensure the FastAPI backend is running.")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")

# --- Sidebar ---
with st.sidebar:
    st.header("🌦️ Application Architecture")
    st.info(
        "Uses a pre-trained **XGBoost Classifier** deployed via **FastAPI** for predicting rain.\n\n"
        "**Theme:** Dark Mode, High Contrast"
    )
    st.header("⚙️ API Debug Tools")
    if st.button("Re-Check API Health", use_container_width=True):
        try:
            response = requests.get(f"{API_URL}/health")
            if response.status_code == 200:
                st.success("API is healthy!")
            else:
                st.warning(f"API returned status {response.status_code}")
            st.json(response.json())
        except:
            st.error("API not reachable. Is your Uvicorn server running?")
    st.markdown("---")
    st.markdown("_Developed for educational deployment purposes._")