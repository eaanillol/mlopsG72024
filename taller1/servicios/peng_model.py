# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 18:10:27 2024

@author: crist
"""
import numpy as np
import pandas as pd
from typing import List
from pydantic import BaseModel
from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from imblearn.ensemble import BalancedRandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
#from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score

# 2. Class which describes a single flower measurements
class penguin_data(BaseModel):
    culmen_length_mm: List[float]
    culmen_depth_mm: List[float] 
    flipper_length_mm: List[float]
    body_mass_g: List[float]
    sex: List[str]
    delta15N: List[float]
    delta13C: List[float]

class PenguinModel:
    # 6. Class constructor, loads the dataset and loads the model
    #    if exists. If not, calls the _train_model method and 
    #    saves the model
    def __init__(self):
        self.df = pd.read_csv("penguins_lter.csv")
        self.model = self._train_model()

    # 4. Perform model training using the RandomForest classifier
    def _train_model(self):

        self.df.drop(['studyName','Sample Number','Region','Island','Stage','Individual ID','Clutch Completion',
               'Date Egg', 'Comments'], axis=1, inplace = True)
        self.df.replace(".",np.nan,inplace = True)
        self.df['Sex'] = self.df['Sex'].astype('category')
        self.df['Species'] = self.df['Species'].astype('category')

        X = self.df.drop(columns='Species')
        y = self.df['Species']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=54)
        
        
        penguins_char = self.df.select_dtypes(include="category").drop(['Species'], axis=1).columns
        
        penguins_num = self.df.select_dtypes(exclude="category").columns
        
        ### Definición del método de desbalanceo mediante SMOTETomek
        
        #sample = SMOTETomek(random_state=0,sampling_strategy='minority')
        
        ### Definición de Pipelines para variables categóricas y numéricas. Procesamiento para imputaciòn y estandarización
        
        numeric_transformer = Pipeline(
            steps=[("imputer", KNNImputer(n_neighbors=15)), ("scaler", StandardScaler())]
        )
        
        categorical_transformer = Pipeline(
            steps=[('imputer', SimpleImputer(strategy='most_frequent',missing_values=np.nan)),
                   ('onehot', OneHotEncoder(drop='first'))]
        )
        
        ### Preprocesamiento para unión de las variables categóricas y numéricas.
        
        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, penguins_num),
                ("cat", categorical_transformer, penguins_char),
            ]
            )
        
        ### Se generó un pipeline que incluía el procesamiento de las variables categóricas y numéricas (pipelines anteriores), adicionalmente que generara un desbalanceo de los datos 
        ### y que generara el modelo tipo Balanced Random Forest.
        clf3 = Pipeline(
            steps=[("preprocessor", preprocessor), ("BRF", BalancedRandomForestClassifier())])
        
        model = clf3.fit(X_train, y_train)
        
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
        data_in = pd.DataFrame(data_in)
        prediction = self.model.predict(data_in)
        return prediction
