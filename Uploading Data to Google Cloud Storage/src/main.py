import requests
import header as h
import pandas as pd
import os
from os import listdir
from os.path import isfile, join

from google.cloud import storage

# Download files from an url
print('='*60,'\n Downloading Files\n','='*60)
for i in range(len(h.filenames)):
    URL = h.urls[i]
    response = requests.get(URL)
    open("./Datasets/Descarga/{}.json.gz".format(h.filenames[i]), "wb").write(response.content)
    print(h.filenames[i],'Downloaded!')

# Listing files to be chunked
onlyfiles = [f for f in listdir('./Datasets/Descarga/') if isfile(join('./Datasets/Descarga/', f))]
# Chunking files
print('='*60,'\n Chunking Files\n','='*60)
for i in range(len(onlyfiles)):
    if(onlyfiles[i]!='.gitkeep'):
        h.getChunkDF('./Datasets/Descarga/',onlyfiles[i],500000,type = '.csv')
        print(onlyfiles[i],'Chunked!')

# Listing files to Replace Nulls
onlyfiles = [f for f in listdir('./Datasets/CSVs/') if isfile(join('./Datasets/CSVs/', f))]
# Replancing nulls in files
print('='*60,'\n Basic ETL\n','='*60)
for i in range(len(onlyfiles)):
    if (onlyfiles[i] != '.gitkeep'):
        df = h.ReemplazarNulos('./Datasets/CSVs/',onlyfiles[i])
        df.to_csv('./Datasets/ETL/{}'.format(onlyfiles[i]),index=False)
        print('ETL:',onlyfiles[i],'---> Replacing nulls')

# Listing files to create their own Date column 
onlyfiles = [f for f in listdir('./Datasets/ETL/') if isfile(join('./Datasets/ETL/', f))]
# Spliting helpful column and creating Date column
print('='*60)
for i in range(len(onlyfiles)):
    if onlyfiles[i] != '.gitkeep':
        df = h.helpful_Fecha('./Datasets/ETL/',onlyfiles[i])
        df.to_csv('./Datasets/ETL/{}'.format(onlyfiles[i]),index=False)
        print('ETL:',onlyfiles[i],'---> Spliting Helpfull and making Date column')

# Uploading files to Google Cloud Storage
print('='*60,'\n Google Cloud Storage\n','='*60)
# Create a new bucket
h.create_bucket('bucket-pf-henry')

# Accessing a specific bucket
my_bucket = h.storage_client.get_bucket('bucket-pf-henry')

# Listing files to upload
onlyfiles = [f for f in listdir('./Datasets/ETL/') if isfile(join('./Datasets/ETL/', f))]

# Uploading files
for i in range(len(onlyfiles)):
    if onlyfiles[i]!='.gitkeep':
        h.upload_to_bucket(onlyfiles[i],'./Datasets/ETL/{}'.format(onlyfiles[i]),'bucket-pf-henry')
        print(onlyfiles[i],'uploaded!')