# mlopsG72024
Curso de MLOPs

El programa se compone de 3 archivos:

1. data_prep.py: en este programa se realiza el preprocesamiento de los datos y el entrenamiento de los modelos.
     -   Como paso inicial se carga el archivo "penguins_lter.csv", al que posteriormente, como primer paso del preprocesamiento, se le eliminan las variables que no serán utilizadas para entrenar el modelo.
     -   En segundo lugar, se reemplazan aquellas variables que se consideran como ruido por np.nan. En el caso de este dataset solo se observó que  algunas de las entradas de la variable "Sex" eran populadas por el valor "."
     -   En Tercer lugar, se realizó el cambio de variables de Objeto a categorica para "Species" y "Sex"
     -   Posteriormente el dataset fue dividido en subgrupos Train y test, con una relacion 70-30.
     -   Usando el sub-grupo Train, se crearon 2 pipelines para las variables numericas y categoricas en donde, para las variables numericas, se reemplazaron los valores vacios por medio de el metodo K vecinos mas cercanos, para utilizar un valor promedio de los datos de aquellas entradas con una similitud mas cercana al valor que se buscaba completar. Para las variables categoricas se utilizó el metodo "SimpleImputter" para reemplazar el valor faltante por el valor mas común para utilizar el meotodo OneHotEncoder para codificar dichas variables.
     -   Finalmente se utilizó la función ColumnTransformer para concatenar los datos categoricos y numericos en un unico dataset, dado que habian sido previamente separados para implementar los pipelines para cada categoria (num, cat).
