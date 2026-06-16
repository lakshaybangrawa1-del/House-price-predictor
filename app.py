import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# Set page configuration
st.set_page_config(
    page_title="Ghar Ke Keemat Predictor",
    page_icon="🏠",
    layout="centered"
)

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv('Housing.csv')
    return df

df = load_data()

# Data Preprocessing
binary_columns = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
for col in binary_columns:
    df[col] = df[col].map({'yes': 1, 'no': 0})

df['furnishingstatus'] = df['furnishingstatus'].map({'furnished': 2, 'semi-furnished': 1, 'unfurnished': 0})

# Features and Target
X = df[['area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'parking', 'prefarea', 'furnishingstatus']]
y = df['price']

# Train Model
model = LinearRegression()
model.fit(X, y)

# --- Streamlit User Interface (Back to Hinglish!) ---

st.title("🏠 House Price Prediction Model")
st.write("Apne ghar ki details daalein aur AI se uski sahi keemat pata karein.")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    area = st.number_input("Ghar ka Total Area (sq. ft. me)", min_value=500, max_value=20000, value=4000, step=100)
    bedrooms = st.slider("Kitne Bedrooms chahiye?", min_value=1, max_value=6, value=3)
    bathrooms = st.slider("Kitne Bathrooms chahiye?", min_value=1, max_value=4, value=2)
    stories = st.slider("Ghar me kitne Floors/Manzil honge?", min_value=1, max_value=4, value=2)
    parking = st.slider("Parking Spaces (Kitni 4 wheeler ki jagah)?", min_value=0, max_value=3, value=1)
    
with col2:
    mainroad = st.selectbox("Ghar Main Road par hai?", ["Yes", "No"])
    guestroom = st.selectbox("Alag se Guestroom chahiye?", ["Yes", "No"])
    basement = st.selectbox("Basement chahiye?", ["Yes", "No"])
    hotwaterheating = st.selectbox("Garam paani (Geyser) ka system chahiye?", ["Yes", "No"])
    airconditioning = st.selectbox("AC (Air Conditioning) chahiye?", ["Yes", "No"])
    prefarea = st.selectbox("Ghar VVIP/Preferred Area me chahiye?", ["Yes", "No"])

furnishingstatus = st.selectbox("Ghar ka Furnishing Status kya hoga?", ["Fully Furnished", "Semi-Furnished", "Unfurnished"])

# Mapping back to numbers
mainroad_val = 1 if mainroad == "Yes" else 0
guestroom_val = 1 if guestroom == "Yes" else 0
basement_val = 1 if basement == "Yes" else 0
hotwaterheating_val = 1 if hotwaterheating == "Yes" else 0
airconditioning_val = 1 if airconditioning == "Yes" else 0
prefarea_val = 1 if prefarea == "Yes" else 0

furnish_map = {"Fully Furnished": 2, "Semi-Furnished": 1, "Unfurnished": 0}
furnishingstatus_val = furnish_map[furnishingstatus]

st.markdown("---")

# Predict Button
if st.button("💰 Ghar Ki Keemat Pata Karein", type="primary"):
    input_features = [[
        area, bedrooms, bathrooms, stories, mainroad_val, 
        guestroom_val, basement_val, hotwaterheating_val, 
        airconditioning_val, parking, prefarea_val, furnishingstatus_val
    ]]
    
    prediction = model.predict(input_features)[0]
    
    # Celebration!
    st.balloons()
    st.success(f"### 🎯 Estimated Market Value: ₹ {prediction:,.2f}")
    
    # Lakhs/Crores display
    if prediction >= 10000000:
        st.info(f"Matalab Lagbhag: **{prediction/10000000:.2f} Crore** 👑")
    elif prediction >= 100000:
        st.info(f"Matalab Lagbhag: **{prediction/100000:.2f} Lakh** 💰")