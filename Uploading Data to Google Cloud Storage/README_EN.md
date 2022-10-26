# Pipeline: Download and Upload data

In this section, the method applied to save the initial datasets in the selected database is disclosed. In this case we will use Google Cloud Storage services, which allow us to store information (datasets) in containers called buckets.
<hr>

## 0. The original datasets

The original datasets are saved on the official page of [Stanford Network Analysis Project](http://snap.stanford.edu/data/web-Amazon.html), which are compressed and saved in .json format.

![1666739501212](image/README/1666739501212.png)
<hr>

## 1. Datasets download

Downloading data is done by iterating the following function:

```python
response = requests.get(URL) # URL of dataset
    open("./ExampleDownload.json.gz", "wb").write(response.content)
```

Once downloaded the files will automatically appear in the Downloads folder

![1666741711947](image/README/1666741711947.png)
<hr>

## 2. Chunk of datasets

Once the original files have been downloaded and saved, each one is fragmented into subfiles of 500,000 rows, using the .csv format.

To do this, iterate the function:

```python
h.getChunkDF('./Datasets/Downloads/',onlyfiles[i],500000,type = '.csv')
```

Getting at the end subfiles in the CSVs folder:

![1666741984496](image/README/1666741984496.png)
<hr>

## 4. Basic ETL to Fragments

The fragments are passed through a transformation stage, which consists of filling cells with null values ​​and separating the helpfull column into .

This is done by iterating the following functions:<br>
```python
# Replacing Nulls
df = h.ReplaceNulls('./Datasets/CSVs/','Example.csv')

# Spliting helpful and Creating Date Column
df = h.helpfulAndDate('./Datasets/ETL/','Example.csv')
```
Original Data:<br>
![1666743887915](image/README/1666743887915.png)

Transformated Data:<br>
![1666743964876](image/README/1666743964876.png)
<hr>

## 5. Uploading Fragments to Google Cloud Storage

The chunked files are uploaded to a specific bucket dedicated to this project, called [bucket-pf-henry](https://console.cloud.google.com/storage/browser/bucket-pf-henry;tab=objects? forceOnBucketsSortingFiltering=false&project=pf-henry-365404&prefix=&forceOnObjectsSortingFiltering=true).

To load the processed files, the following function is iterated:

```python
h.upload_to_bucket(onlyfiles[i],'./Datasets/ETL/ExampleFile.csv','bucket-pf-henry')
```

This is how we upload our processed files to the cloud, using Google Cloud Storage services. In order to be able to have a periodic backup of all the data received.

![1666744457547](image/README/1666744457547.png)