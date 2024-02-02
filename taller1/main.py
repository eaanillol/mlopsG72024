# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 20:04:37 2024

@author: crist
"""
# 1. Library imports
from fastapi import FastAPI
from servicios.peng_model import penguin_data, PenguinModel

# 2. Create app and model objects
app = FastAPI()
model = PenguinModel()
# 3. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted flower species with the confidence
@app.post('/predict')
def predict_species(penguin: penguin_data):
    data = penguin.model_dump()
    
    prediction, probability = model.predict_species(
        data['island'], data['culmen_length_mm'], data['culmen_depth_mm'], data['flipper_length_mm'],
        data['body_mass_g'], data['sex']
    )
    return {
        'prediction': prediction,
        'probability': probability
    }