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

# 3. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted flower species with the confidence
@app.post('/predict/{model_id}')
def predict_species(penguin: penguin_data,model_id: int): 
    
    try:
        model = PenguinModel(model_id)
        data = penguin.model_dump()
        prediction = model.predict_species(
        data['culmen_length_mm'], data['culmen_depth_mm'], data['flipper_length_mm'],
        data['body_mass_g'], data['sex'],data['delta15N'], data['delta13C'])
    except ValueError as e:
        return {
                    "message": str(e)
               }
    except:
        return {
                    "message": "Something went wrong!!!"
               }
    return {
        'prediction': prediction
    }
