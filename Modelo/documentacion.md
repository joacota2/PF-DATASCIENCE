# Documentación:

En **metadata.ipynb** se encuentran descriptos los pasos que conforman extraccion, transformacion y carga de los metadatos pertinentes  del proyecto.

--

En **allreviews.ipynb** se encuentran descriptos los pasos que conforman extraccion, transformacion y carga de las tablas de reseñas pertinentes  del proyecto.

--

En **modelo.ipynb** se encuentran descriptos los pasos que conforman  analisis, entrenamiento, evaluacion y optimizacion del sistema de recomendacion.

## Extraccion y transformacion:

1. Ingestamos las tablas provenientes de  http://snap.stanford.edu/.
2. Sobre las tablas **review** (24 tablas / 18M registros):

* Agregamos columnas categoryName y category.
* Expandimos la columna helpful [y/n].
* Concatenamos las 24 tablas en 1 llamada allreviews.

3. Sobre la tabla **metadata**(1 tabla / 10M registros):

* Expandimos la columna salesRank {'category': rank}.
* Expandimos la columna related a also_bought, also_viewed, buy_after_viewing, bought_together.

## Carga:

1. Fraccionamos las tablas en chunks de 1.000.000 de registros.
2. Realizamos la carga de los mismos a BigQuery utilizando pandas .to_gbq.

## Analisis:

1. Ingestamos la informacion necesaria para el modelado desde BigQuery
2. Obtuvimos una serie de metricas que consideramos relevantes para el modelado:

* Total de usuarios unicos.
* Distribucion de calificaciones de productos agrupadas por usuario.
* Distribución de calificaciones agrupadas por puntaje.
* Productos ordenados por popularidad.
* Distribución de total de reseñas por producto.
* Creamos un filtro para productos con pocas interacciones.

## Modelado:

1. Instanciamos un modelo de **Descomposición en Valores Singulares(SVD)**.
2. Separamos los registros de entrenamiento (%75) y de testeo (%25)
3. Entrenamos y realizamos predicciones de prueba sobre usuarios particulares.

## Evaluacion:

1. Testeamos las predicciones sobre el conjunto de testeo, obtuvimos:

* RMSE: 0.9568
* Accuracy:  0.9567

## Optimizacion:

1. Realizamos Validacion cruzada para determinar el N de factores convenientes para el SVD.
2. Ploteamos desempeño según cantidad de factores de SVD
3. Realizamos un GridSearch para explorar en profundidad mas hiperparametros.
4. Resultados:

* RMSE: 0.9591955534336384.
* BEST PARAMS: {'n_factors': 5, 'n_epochs': 20, 'lr_all': 0.005, 'reg_all': 0.02}

## Enlaces:

etl: https://pandas.pydata.org/docs/

etl: https://numpy.org/doc/

etl: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_gbq.html

analisis: https://matplotlib.org/stable/index.html

modelado: https://scikit-learn.org/stable/

may help:

https://holowczak.com/python-programming-with-google-bigquery/8/?doing_wp_cron=1665680483.7020699977874755859375

https://www.youtube.com/watch?v=ajTp60neMlc&t=119s

https://www.youtube.com/watch?v=S0wNWOR4WoE

https://www.youtube.com/watch?v=sEx8RwvT_-8

https://www.youtube.com/watch?v=sEx8RwvT_-8
