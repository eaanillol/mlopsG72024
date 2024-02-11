# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 18:10:27 2024

@author: crist
"""
import joblib
import numpy as np
import pandas as pd
import sklearn as skm
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.linear_model import LogisticRegression
from imblearn.ensemble import BalancedRandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
#from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score


penguins = pd.read_csv("penguins_lter.csv")

penguins.drop(['studyName','Sample Number','Region','Island','Stage','Individual ID','Clutch Completion',
               'Date Egg', 'Comments'], axis=1, inplace = True)

penguins.replace(".",np.nan,inplace = True)
penguins['Sex'] = penguins['Sex'].astype('category')
penguins['Species'] = penguins['Species'].astype('category')

#

X = penguins.drop(columns='Species')
y = penguins['Species']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=54)


penguins_char = X_train.select_dtypes(include="category").columns

penguins_num = X_train.select_dtypes(exclude="category").columns

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


param_grid3 = {'BRF__max_depth': [10, 20, 30, 40, 50],
 'BRF__max_features': ["auto", "sqrt", "log2"],
 'BRF__n_estimators': [100, 200, 400, 50]
}

grid_search = GridSearchCV(clf3, param_grid3, cv=5, refit="f1_score")
grid_search

grid_search.fit(X_train, y_train)

y_pred=grid_search.predict(X_test)
cm=skm.metrics.confusion_matrix(y_test,y_pred)
plt.rcParams.update({'font.size': 16})
cm_display = ConfusionMatrixDisplay(cm)
cm_display = cm_display.plot(cmap=plt.cm.Oranges)

joblib.dump(grid_search, "RF_model.joblib")

## Support vector machine ###

clf2 = Pipeline(
    steps=[("preprocessor", preprocessor), ("SVM", SVC())])

clf2.fit(X_train, y_train)

y_pred=clf2.predict(X_test)
cm=skm.metrics.confusion_matrix(y_test,y_pred)
plt.rcParams.update({'font.size': 16})
cm_display = ConfusionMatrixDisplay(cm)
cm_display = cm_display.plot(cmap=plt.cm.Blues)

joblib.dump(clf2, "SVM_model.joblib")

## Logistic regression ###

clf1 = Pipeline(
    steps=[("preprocessor", preprocessor), ("LR", LogisticRegression(random_state=0))])

clf1.fit(X_train, y_train)

y_pred=clf1.predict(X_test)
cm=skm.metrics.confusion_matrix(y_test,y_pred)
plt.rcParams.update({'font.size': 16})
cm_display = ConfusionMatrixDisplay(cm)
cm_display = cm_display.plot(cmap=plt.cm.Blues)

joblib.dump(clf2, "Regression_model.joblib")


