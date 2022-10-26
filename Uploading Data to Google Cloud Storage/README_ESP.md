# Pipeline Descarga y Carga de datos

En esta sección, se da a conocer el método aplicado para guardar los datasets iniciales en la base de datos seleccionada. En este caso utilizaremos los servicios de Google Cloud Storage, los cuales nos permiten guardar información (datasets) en contenedores denominados buckets.

## 0. Los datasets originales

Como es de conocimiento, los datasets originales estan guardados en la página oficial de [Stanford Network Analysis Project](http://snap.stanford.edu/data/web-Amazon.html), los cuales están comprimidos y guardados en formato .json.

![1666739501212](image/README/1666739501212.png)

## 1. Descarga de datasets

La descarga de datos se realiza mediante la iteración de la siguiente función:

```python
response = requests.get(URL) # URL of dataset
    open("./ExampleDownload.json.gz", "wb").write(response.content)
```

Una vez descargados los archivos apareceran automaticamente en la carpeta Downloads

![1666741711947](image/README/1666741711947.png)

## 2. Fragmentando datasets

Una vez descargados y guardados los archivos originales se procede a fragmentar cada archivo en subarchivos de 500000 filas cada uno, cada uno en formato .csv

Para ello se itera la función:

```python
h.getChunkDF('./Datasets/Downloads/',onlyfiles[i],500000,type = '.csv')
```

Obteniendo al final subarchivos en la carpeta CSVs:

![1666741984496](image/README/1666741984496.png)

## 4. ETL básico a los fragmentos

Los fragmentos son pasados por una etapa de transformación, la cual consiste en rellenar celdas con valores nulos y la separación de la columna helpfull en .

Esto se realiza iterando las siguientes funciones:<br>
```python
# Replacing Nulls
df = h.ReplaceNulls('./Datasets/CSVs/','Example.csv')

# Spliting helpful and Creating Date Column
df = h.helpfulAndDate('./Datasets/ETL/','Example.csv')
```
Original Data:<br>
![1666743887915](image/README/1666743887915.png)

Transformation:<br>
![1666743964876](image/README/1666743964876.png)


## 5. Cargando fragmentos a Google Cloud Storage

Los archivos fragmentados se suben a un bucket específico dedicado para el presente proyecto, denominado [bucket-pf-henry](https://console.cloud.google.com/storage/browser/bucket-pf-henry;tab=objects?forceOnBucketsSortingFiltering=false&project=pf-henry-365404&prefix=&forceOnObjectsSortingFiltering=true).

Para cargar los archivos procesados, se itera la siguiente función:

```python
h.upload_to_bucket(onlyfiles[i],'./Datasets/ETL/ExampleFile.csv','bucket-pf-henry')
```

Es así como cargamos nuestros archivos procesados en la nube, utilizando los servicios de Google Cloud Storage. Con la finalidad de poder tener un backup periodico de toda la data recepcionada.

![1666744457547](image/README/1666744457547.png)