# Load the libraries
from fastapi import FastAPI, HTTPException
from joblib import load
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
import pickle

# Load the model
loaded_model = pickle.load(open('ml_model.pkl', 'rb'))

# Initialize an instance of FastAPI
app = FastAPI()

# Define the default route 
@app.get("/")
def root():
    return {"message": "Welcome to Your Volume prediction FastAPI"}


 # Define the route to the sentiment predictor
@app.post("/predict")
def predict(text_message):

    if(not(text_message)):
        raise HTTPException(status_code=400, 
                            detail = "Please Provide a valid text message")

    vol_moving_avg = float(text_message.split('&')[0].split('=')[1])
    adj_close_rolling_med = float(text_message.split('&')[1].split('=')[1])
    input_feature = np.array([vol_moving_avg, adj_close_rolling_med]).reshape(1, 2)

    # feature transformation
    poly = PolynomialFeatures(degree=2, include_bias=True)
    input_feature_poly = poly.fit_transform(input_feature)
    
    prediction = round(loaded_model.predict(input_feature_poly)[0], 2)

    return {"Volume prediction": prediction}