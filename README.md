# mlopsG72024
Curso de MLOPs

El programa se compone de 3 archivos:

1. data_prep.py: en este programa se realiza el preprocesamiento de los datos y el entrenamiento de los modelos.
     -   Como paso inicial se carga el archivo "penguins_lter.csv", al que posteriormente, como primer paso del preprocesamiento, se le eliminan las variables que no serán utilizadas para entrenar el modelo.
     -   En segundo lugar, se reemplazan aquellas variables que se consideran como ruido por np.nan. En el caso de este dataset solo se observó que  algunas de las entradas de la variable "Sex" eran populadas por el valor "."
     -   En Tercer lugar, se realizó el cambio de variables de Objeto a categórica para "Species" y "Sex"
     -   Posteriormente el dataset fue dividido en subgrupos Train y test, con una relacion 70-30.
     -   Usando el subgrupo Train, se crearon 2 pipelines para las variables numéricas y categóricas en donde, para las variables numéricas, se reemplazaron los valores vacíos por medio del método K vecinos más cercanos, para utilizar un valor promedio de los datos de aquellas entradas con una similitud más cercana al valor que se buscaba completar. Para las variables categóricas se utilizó el método "SimpleImputter" para reemplazar el valor faltante por el valor más común, luego se implementó el método OneHotEncoder para codificar dichas variables.
     -   Como último paso se utilizó la función ColumnTransformer para concatenar los datos categóricos y numéricos en un único dataset, dado que habían sido previamente separados para implementar los pipelines para cada categoría (num, cat).
     -   ENTRENAMIENTO: Para cargar cada uno de los 3 modelos se utilizó un Pipeline para implementar los pasos de preprocesamiento a los datos de entrada y luego implementar el modelo. Para el modelo Random forest se utilizo la función GridSearch para seleccionar los parámetros que dieran el mejor valor de f1_score. Para los demás modelos solo se implementó un pipeline y se utilizaron los hiperparametros por defecto. Cada modelo, incluyendo el Pipeline, fue guardado usando la librería joblib.

2. peng_model.py: En este archivo se definen las variables de entrada del programa, y se crea la clase Penguinmodel que contiene las funciones _load_model y predict_species.
     - _load_model: carga el modelo .joblib mediante...
     - predict_species: realiza la predicción de la especie del pinguino en función de las variables de entrada definidas por usuario y retorna la especie predecida. antes de utilizarse los datos, estos son convertidos en un Dataframe para luego ser ingresados al modelo previamente entrenado.

3. main.py
4. Dockerfile
5. requirements.txt
6. PASOS PARA EJECUTAR EL PROGRAMA
   
