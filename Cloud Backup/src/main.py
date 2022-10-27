import requests
import header as h
import pandas as pd
from os import listdir
from os.path import isfile, join
import compress_json
import json


# Download files from an url
print('='*60,'\n Downloading Files\n','='*60)
for i in range(6): # Change to obtain all files: for i in range(len(h.filenames)):
    URL = h.urls[i]
    response = requests.get(URL)
    open("./Datasets/Downloads/{}.json.gz".format(h.filenames[i]), "wb").write(response.content)
    print(h.filenames[i],'Downloaded!')

# Listing files to be chunked
onlyfiles = [f for f in listdir('./Datasets/Downloads/') if isfile(join('./Datasets/Downloads/', f))]
print(onlyfiles)
# Chunking files
fileFormat = '.json'
print('='*60,'\n Chunking Files\n','='*60)
for i in range(len(onlyfiles)):
    if(onlyfiles[i]!='.gitkeep'):
        h.getChunkDF('./Datasets/Downloads/',onlyfiles[i],500000)
        print(onlyfiles[i],'Chunked!')

# Listing files to Replace Nulls
onlyfiles = [f for f in listdir('./Datasets/CSVs/') if isfile(join('./Datasets/CSVs/', f))]
# Replancing nulls in files
print('='*60,'\n Basic ETL\n','='*60)
for i in range(len(onlyfiles)):
    if (onlyfiles[i] != '.gitkeep'):
        df = h.ReplaceNulls('./Datasets/CSVs/',onlyfiles[i])
        df.to_csv('./Datasets/ETL/{}'.format(onlyfiles[i]),index=False)
        print('ETL:',onlyfiles[i],'---> Replacing nulls')

# Listing files to create their own Date column
onlyfiles = [f for f in listdir('./Datasets/ETL/') if isfile(join('./Datasets/ETL/', f))]
# Spliting helpful column and creating Date column
print('='*60)
for i in range(len(onlyfiles)):
    if onlyfiles[i] != '.gitkeep':
        df = h.helpfulAndDate('./Datasets/ETL/',onlyfiles[i])
        df.to_csv('./Datasets/ETL/{}'.format(onlyfiles[i]),index=False)
        print('ETL:',onlyfiles[i],'---> Spliting Helpfull and making Date column')

# Listing files to be compressed
onlyfiles = [f for f in listdir('./Datasets/ETL/') if isfile(join('./Datasets/ETL/', f))]
print(onlyfiles)
print('='*60,'\n Compressing transformated files\n','='*60)
for i in range(len(onlyfiles)):
    if onlyfiles[i] != '.gitkeep':
        df = pd.read_csv('./Datasets/ETL/{}'.format(onlyfiles[i]))
        df.to_json('./Datasets/Compressed_Files/{}'.format(onlyfiles[i]).replace('.csv','.json.gz'),orient='records',lines=True,compression="gzip")
        print(onlyfiles[i],'Compressed!')

# Uploading files to Google Cloud Storage
print('='*60,'\n Google Cloud Storage\n','='*60)
# Create a new bucket
h.create_bucket('bucket-pf-henry')

# Accessing a specific bucket
my_bucket = h.storage_client.get_bucket('bucket-pf-henry')

# Listing files to upload
onlyfiles = [f for f in listdir('./Datasets/Compressed_Files/') if isfile(join('./Datasets/Compressed_Files/', f))]

# Uploading files
for i in range(len(onlyfiles)):
    if onlyfiles[i]!='.gitkeep':
        h.upload_to_bucket(onlyfiles[i],'./Datasets/Compressed_Files/{}'.format(onlyfiles[i]),'bucket-pf-henry')
        print(onlyfiles[i],'uploaded!')    