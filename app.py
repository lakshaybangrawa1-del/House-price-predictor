import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# Set page configuration
st.set_page_config(
    page_title="House Price Predictor, Jaipur",
    page_icon="👑",
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

# --- Streamlit User Interface ---

st.title("House Price Predictor, Jaipur")
st.write("Apne Ghar ki details daalein aur keemat pata karein.")
st.markdown("---")

locality = st.selectbox("Locality", ["Jagatpura (Ultra Premium)", "Mansarovar (VIP)", "Other Premium Areas"])

col1, col2 = st.columns(2)

with col1:
    area = st.number_input("Ghar ka Total Area (sq. ft. me)", min_value=500, max_value=20000, value=1500, step=100)
    bedrooms = st.slider("Kitne Bedrooms chahiye?", min_value=1, max_value=6, value=3)
    bathrooms = st.slider("Kitne Bathrooms chahiye?", min_value=1, max_value=4, value=2)
    stories = st.slider("Ghar me kitne Floors/Manzil honge?", min_value=1, max_value=4, value=1)
    
with col2:
    parking = st.slider("Parking Spaces (Kitni gaadiyo ki jagah)?", min_value=0, max_value=3, value=1)
    mainroad = st.selectbox("Ghar Main Road par hai?", ["Yes", "No"])
    guestroom = st.selectbox("Alag se Guestroom chahiye?", ["Yes", "No"])
    basement = st.selectbox("Basement chahiye?", ["Yes", "No"])

col3, col4 = st.columns(2)
with col3:
    hotwaterheating = st.selectbox("Garam paani (Geyser) ka system chahiye?", ["Yes", "No"])
with col4:
    prefarea = st.selectbox("Ghar VVIP/Preferred Area me chahiye?", ["Yes", "No"])

furnishingstatus = st.selectbox("Ghar ka Furnishing Status kaisa hoga?", ["Fully Furnished", "Semi-Furnished", "Unfurnished"])

# Mapping responses back to numbers
mainroad_val = 1 if mainroad == "Yes" else 0
guestroom_val = 1 if guestroom == "Yes" else 0
basement_val = 1 if basement == "Yes" else 0
hotwaterheating_val = 1 if hotwaterheating == "Yes" else 0
prefarea_val = 1 if prefarea == "Yes" else 0
airconditioning_val = 1  

furnish_map = {"Fully Furnished": 2, "Semi-Furnished": 1, "Unfurnished": 0}
furnishingstatus_val = furnish_map[furnishingstatus]

st.markdown("---")

# Predict Button
if st.button("👑 VIP Keemat Pata Karein", type="primary"):
    # Base Premium Rate as per your choice
    base_rate_per_sqft = 5000  # ₹5000 per sq. ft.
        
    # Feature multipliers for luxury additions
    feature_multiplier = 1.0
    if bedrooms > 3: feature_multiplier += 0.05
    if bathrooms > 1: feature_multiplier += 0.05
    if mainroad_val == 1: feature_multiplier += 0.05
    if prefarea_val == 1: feature_multiplier += 0.10
    if furnishingstatus_val == 2: feature_multiplier += 0.05
    
    vip_prediction = (area * base_rate_per_sqft) * feature_multiplier
    
    # Celebration!
    st.balloons()
    st.success(f"### 🎯 Estimated Market Value: ₹ {vip_prediction:,.2f}")
    
    # Lakhs/Crores display
    if vip_prediction >= 10000000:
        st.info(f"Matalab Lagbhag: **{vip_prediction/10000000:.2f} Crore** 👑💸")
    elif vip_prediction >= 100000:
        st.info(f"Matalab Lagbhag: **{vip_prediction/100000:.2f} Lakh** 💰")
