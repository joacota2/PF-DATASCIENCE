# Documentación:


On **metadata.ipynb** there´s the description of the work on extraction, transformation and loading of the metadata relevant to this project.

--

On **allreviews.ipynb** there´s the description of the work on extraction, transformation and loading of the reviews relevant to this project.

--

On **modelo.ipynb** there´s a description of the work on analysis, training, evaluation and optimization of the recomendation system

## Extraction y Transformation:

1. Ingested the data from:  http://snap.stanford.edu/.
2. On **review** (24 tables / 18M registry):

* Added columns categoryName y category.
* Expanded column helpful [y/n].
* Concat the 24 tables on 1 called allreviews.

3. On  **metadata**(1 table / 10M registry):

* Expanded the column salesRank {'category': rank}.
* Expanded the column related to also_bought, also_viewed, buy_after_viewing, bought_together.

## Carga:

1. Partitioned the tables to chunks of 1.000.000 rows.
2. Load those to  BigQuery using pandas .to_gbq.

## Analysis:

1. Ingested the data needed for the model from BigQuery
2. Obtained some metrics that considered relevant for the model:

* Total of unique users.
* Distribution of products qualifications grouped by users.
* Distribution of qualifications grouped by Score.
* Products ordered by Popularity.
* Distribution of total reviews by product.
* Created a filter for products with low interactions.

## Modeling:

1. Instanced a model of  **Singular Value Decomposition(SVD)**.
2. Split training registry (%75) and testing (%25).
3. Trained and predicted on random individuals.

## Testing:

1.Tested the predictions on the TestSet, Got:

* RMSE: 0.9568
* Accuracy:  0.9567

## Optimization:

1. Ran Cross Validation on the model to figure out the most convenient N factors for the SVD.
2. Plot all Cross Validation results.
3. Ran a GridSearch to tweak further other Hiper Parameters.
4. Results:

* RMSE: 0.9591955534336384.
* BEST PARAMS: {'n_factors': 5, 'n_epochs': 20, 'lr_all': 0.005, 'reg_all': 0.02}

## Links:

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
