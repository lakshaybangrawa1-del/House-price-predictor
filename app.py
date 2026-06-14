import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# 1. Page Config
st.set_page_config(page_title="House Price Predictor", layout="centered")
st.title("🏡 Ghar Ki Keemat Predict Karne Wala AI")
st.write("Apne ghar ki details daliye aur AI se sahi keemat janiye!")

# 2. Model Training (Ekdum simple assignment se)
@st.cache_resource
def get_trained_model():
    df = pd.read_csv('Housing.csv')
    
    # Yes/No ko 1/0 me badalna
    binary_columns = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
    for col in binary_columns:
        df[col] = df[col].map({'yes': 1, 'no': 0})
        
    # Furnishing Status ko bina get_dummies ke sidhe map karna (Error free tarika)
    # furnished = 0, semi-furnished = 1, unfurnished = 2 (Model sequence ke hisab se dummy mapping)
    df['furnishingstatus_semi-furnished'] = df['furnishingstatus'].apply(lambda x: 1 if x == 'semi-furnished' else 0)
    df['furnishingstatus_unfurnished'] = df['furnishingstatus'].apply(lambda x: 1 if x == 'unfurnished' else 0)
    
    # Purana text column drop kar dena
    df = df.drop('furnishingstatus', axis=1)
    
    X = df.drop('price', axis=1)
    y = df['price']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

# Model load karna
model = get_trained_model()

# 3. Form Inputs
st.header("📋 Ghar Ki Details Bharein")
col1, col2 = st.columns(2)

with col1:
    area = st.number_input("Ghar Ka Area (Sq Ft me):", min_value=100, max_value=20000, value=5000, step=50)
    bedrooms = st.slider("Bedrooms Ki Ginti:", min_value=1, max_value=6, value=3)
    bathrooms = st.slider("Bathrooms Ki Ginti:", min_value=1, max_value=5, value=2)
    stories = st.slider("Manzil (Stories):", min_value=1, max_value=4, value=2)
    parking = st.slider("Parking Space (Gaadiyo ki ginti):", min_value=0, max_value=3, value=1)

with col2:
    mainroad = st.selectbox("Kya ghar Main Road par hai?", ["Yes", "No"])
    guestroom = st.selectbox("Kya ghar me Guestroom hai?", ["Yes", "No"])
    basement = st.selectbox("Kya ghar me Basement hai?", ["Yes", "No"])
    hotwaterheating = st.selectbox("Kya Hot Water Geyser/Heating hai?", ["Yes", "No"])
    airconditioning = st.selectbox("Kya ghar me AC laga hai?", ["Yes", "No"])
    prefarea = st.selectbox("Kya ghar posh/Preferred Area me hai?", ["Yes", "No"])

furnishing = st.selectbox("Furnishing Status Kya Hai?", ["Semi-Furnished", "Unfurnished", "Fully-Furnished"])

# 4. Dropdown data ko numbers me convert karna
mainroad_val = 1 if mainroad == "Yes" else 0
guestroom_val = 1 if guestroom == "Yes" else 0
basement_val = 1 if basement == "Yes" else 0
hotwaterheating_val = 1 if hotwaterheating == "Yes" else 0
airconditioning_val = 1 if airconditioning == "Yes" else 0
prefarea_val = 1 if prefarea == "Yes" else 0

# Ekdum safe string check python standard dropdown ke liye
semi_furnished_val = 1 if furnishing == "Semi-Furnished" else 0
unfurnished_val = 1 if furnishing == "Unfurnished" else 0

# 5. Predict Button
if st.button("💰 Ghar Ki Keemat Pata Karein"):
    user_inputs = [[area, bedrooms, bathrooms, stories, mainroad_val, guestroom_val, 
                    basement_val, hotwaterheating_val, airconditioning_val, parking, 
                    prefarea_val, semi_furnished_val, unfurnished_val]]
    
    prediction = model.predict(user_inputs)
    st.balloons()  # Mast celebration balloons
    st.success(f"🎉 AI ke mutabik is ghar ki keemat lagbhag **₹ {prediction[0]:,.2f}** honi chahiye!")