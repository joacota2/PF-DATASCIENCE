# Documentación

En **modelo.ipynb se encuentran descriptos los pasos llevados a cabo en el preprocesamiento, entrenamiento, evaluacion y prediccion del modelo.**

## Preprocesamiento:

1. Ingestamos las tablas provenientes de  http://snap.stanford.edu/
2. Sobre las tablas review (24 tablas) eliminamos las columnas:  reviewerName, reviewerID, reviewText, summary, unixReviewTime, reviewTime.
3. Sobre la tabla metadata eliminamos las columnas  price, brand, imUrl, Description.
4. Expandimos la columna related a also_bought, also_viewed, buy_after_viewing, bought_together
5. Normalizamos y convertimos toda la data a valores numericos
6. Creamos versiones reducidas para un pre-entrenamiento

## Entrenamiento:

1. Consideramos matriz de factorizacion y K-vecinos como posibles algoritmos
2. Buscamos mejores hiperparametros

## Evaluación:

---

## Predicción:

---

## Enlaces:

https://holowczak.com/python-programming-with-google-bigquery/8/?doing_wp_cron=1665680483.7020699977874755859375

https://www.youtube.com/watch?v=ajTp60neMlc&t=119s

https://www.youtube.com/watch?v=S0wNWOR4WoE

https://www.youtube.com/watch?v=sEx8RwvT_-8

https://pandas.pydata.org/docs/

https://www.youtube.com/watch?v=sEx8RwvT_-8

https://stackoverflow.com/questions/38231591/split-explode-a-column-of-dictionaries-into-separate-columns-with-pandas
