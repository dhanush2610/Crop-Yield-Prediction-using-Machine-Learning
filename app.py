import streamlit as st
import pandas as pd
import pickle

# Load the trained model and columns
with open("crop_yield_prediction_model.pkl", 'rb') as f:
    model = pickle.load(f)

with open("crop_yield_columns.pkl", 'rb') as f:
    columns = pickle.load(f)

st.title('Crop Yield Prediction')
st.image("img1.jpg",width=710)
st.write("""
Enter the soil, environmental, and crop data to predict crop yield.
""")

# Sidebar - Input parameters
st.sidebar.header('Input Parameters')

def user_input_features():
    Crop = st.sidebar.selectbox('Crop', ['Select Crop','Rice', 'Maize', 'ChickPea', 'KidneyBeans', 'PigeonPeas',
       'MothBeans', 'MungBean', 'Blackgram', 'Lentil', 'Pomegranate',
       'Banana', 'Mango', 'Grapes', 'Watermelon', 'Muskmelon', 'Apple',
       'Orange', 'Papaya', 'Coconut', 'Cotton', 'Jute', 'Coffee'])
    Nitrogen = st.sidebar.slider('Nitrogen content in soil', 0, 100, 0)
    Phosphorus = st.sidebar.slider('Phosphorus content in soil', 0, 100, 0)
    Potassium = st.sidebar.slider('Potassium content in soil', 0, 100, 0)
    Temperature = st.sidebar.slider('Temperature (in Celsius)', 0.0, 50.0, 0.0)
    Humidity = st.sidebar.slider('Humidity (in %)', 0.0, 100.0, 0.0)
    pH = st.sidebar.slider('pH value of soil', 0.0, 14.0, 0.0)
    Rainfall = st.sidebar.slider('Rainfall (in mm)', 0.0, 300.0, 0.0)  # Update with actual crop names
    data = {
        'Crop': Crop,
        'Nitrogen': Nitrogen,
        'Phosphorus': Phosphorus,
        'Potassium': Potassium,
        'Temperature': Temperature,
        'Humidity': Humidity,
        'pH': pH,
        'Rainfall': Rainfall,
    }
    features = pd.DataFrame(data, index=[1])
    return features

input_df = user_input_features()

# One-hot encode the 'Crop' feature
input_df_encoded = pd.get_dummies(input_df, columns=['Crop'])

# Ensure all columns used during training are present
missing_cols = set(columns) - set(input_df_encoded.columns)
for col in missing_cols:
    input_df_encoded[col] = 0
input_df_encoded = input_df_encoded[columns]  # Reorder columns to match training order

# Display user input parameters
st.subheader('User Input Parameters')
st.write(input_df)

# Predicting crop yield
prediction = model.predict(input_df_encoded)

# Display the prediction
st.markdown(f"<h3 style='text-align: left; font-size: 20px;'>Predicted Crop Yield</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: left; font-size: 18px;'>Yield: {prediction[0]:.2f} tons/ha</p>", unsafe_allow_html=True)