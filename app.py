import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# Set page configuration for a professional look
st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="centered"
)

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv('Housing.csv')
    return df

df = load_data()

# Data Preprocessing (Encoding categorical variables)
# Mapping binary columns to 1 and 0
binary_columns = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
for col in binary_columns:
    df[col] = df[col].map({'yes': 1, 'no': 0})

# Mapping furnishingstatus to numbers
df['furnishingstatus'] = df['furnishingstatus'].map({'furnished': 2, 'semi-furnished': 1, 'unfurnished': 0})

# Features and Target variable
X = df[['area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'parking', 'prefarea', 'furnishingstatus']]
y = df['price']

# Train the Linear Regression Model
model = LinearRegression()
model.fit(X, y)

# --- Streamlit User Interface (Proper English) ---

st.title("🏠 House Price Prediction Model")
st.write("Enter the property details below to estimate the market value of the house.")
st.markdown("---")

# Creating layout columns for input fields to make it compact
col1, col2 = st.columns(2)

with col1:
    area = st.number_input("Total Area (in sq. ft.)", min_value=500, max_value=20000, value=4000, step=100)
    bedrooms = st.slider("Number of Bedrooms", min_value=1, max_value=6, value=3)
    bathrooms = st.slider("Number of Bathrooms", min_value=1, max_value=4, value=2)
    stories = st.slider("Number of Stories/Floors", min_value=1, max_value=4, value=2)
    parking = st.slider("Parking Spaces (Car Capacity)", min_value=0, max_value=3, value=1)
    
with col2:
    mainroad = st.selectbox("Main Road Access", ["Yes", "No"])
    guestroom = st.selectbox("Has Guestroom?", ["Yes", "No"])
    basement = st.selectbox("Has Basement?", ["Yes", "No"])
    hotwaterheating = st.selectbox("Has Hot Water Heating?", ["Yes", "No"])
    airconditioning = st.selectbox("Has Air Conditioning?", ["Yes", "No"])
    prefarea = st.selectbox("Located in Preferred Area?", ["Yes", "No"])

furnishingstatus = st.selectbox("Furnishing Status", ["Fully Furnished", "Semi-Furnished", "Unfurnished"])

# Mapping UI string responses back to numerical values for model prediction
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
if st.button("Predict Estimated Price", type="primary"):
    # Create input features array
    input_features = [[
        area, bedrooms, bathrooms, stories, mainroad_val, 
        guestroom_val, basement_val, hotwaterheating_val, 
        airconditioning_val, parking, prefarea_val, furnishingstatus_val
    ]]
    
    # Generate prediction
    prediction = model.predict(input_features)[0]
    
    # Display Result with celebration balloons
    st.balloons()
    st.success(f"### 🎯 Estimated Market Value: ₹ {prediction:,.2f}")
    
    # Optional: Display in Lakhs/Crores for a local touch if needed, but in proper text
    if prediction >= 10000000:
        st.info(f"Approx. **{prediction/10000000:.2f} Crore**")
    elif prediction >= 100000:
        st.info(f"Approx. **{prediction/100000:.2f} Lakh**")