# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 18:10:27 2024

@author: crist
"""
import joblib
import pandas as pd
from pydantic import BaseModel

#from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score

# 2. Class which describes a single flower measurements
class penguin_data(BaseModel):
    culmen_length_mm: float = 39.1
    culmen_depth_mm: float = 18.7
    flipper_length_mm:float = 181
    body_mass_g:float = 3750
    sex: str = "MALE"
    delta15N:float = 8.94956
    delta13C:float = -2.469454
    studyName: str = "PAL0708"
    Sample_Number:float = 1
    Region: str = "Anvers"
    Island: str = "Torgersen"
    Stage:str = "Adult, 1 Egg Stage"
    Individual_ID:str = "N1A1"
    Clutch_Completion:str = "Yes"
    Date_Egg :float = 2017    
    Comments: str = "Not enough blood for isotopes."

class PenguinModel:
    # 6. Class constructor, loads the dataset and loadst he model
    def __init__(self, model_select: int):
        self.df = pd.read_csv("penguins_lter.csv")
        self.model_select = model_select  # Store the selected model number
        self.model = self._load_model()
         
    # 4. Perform model training using the RandomForest classifier
    def _load_model(self):
        if self.model_select == 1:
            model = joblib.load("servicios/RF_model.joblib")
        elif self.model_select == 2:
            model = joblib.load("servicios/SVM_model.joblib") 
        elif self.model_select == 3:
            model = joblib.load("servicios/Regression_model.joblib")
        else:
            raise ValueError("Invalid value for Model_select. Please select from 1, 2, or 3.")
        return model

    # 5. Make a prediction based on the user-entered data
    #    Returns the predicted species with its respective probability
    def predict_species(self, culmen_length_mm, culmen_depth_mm, flipper_length_mm, body_mass_g, sex,
                        delta15N, delta13C):
        data_in = [culmen_length_mm, culmen_depth_mm, flipper_length_mm, body_mass_g, sex,
                   delta15N, delta13C]
        data_in = {'Culmen Length (mm)':data_in[0],'Culmen Depth (mm)':data_in[1],
                   'Flipper Length (mm)':data_in[2],'Body Mass (g)':data_in[3],'Sex':data_in[4],
                   'Delta 15 N (o/oo)':data_in[5],'Delta 13 C (o/oo)':data_in[6]}
        data_in = pd.DataFrame(data_in, index=[0])
        print(data_in)
        prediction = self.model.predict(data_in)
        return prediction[0]
