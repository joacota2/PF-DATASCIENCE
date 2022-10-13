#pip install --upgrade google-cloud-storage

import os
from google.cloud import storage
import _3_strings

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './GCS API/ServiceKey_GoogleCloud.json'

storage_client = storage.Client()

'''
Create a New Bucket
'''
bucket_name = 'bucket-pf-henry'
bucket = storage_client.bucket(bucket_name)
bucket.location = 'US'
#bucket = storage_client.create_bucket(bucket)

'''
Print Bucket Detail
'''
vars(bucket)

'''
Accesing a specific Bucket
'''
my_bucket = storage_client.get_bucket('bucket-pf-henry')

'''
Upload Files
'''
def upload_to_bucket(blob_name, file_path, bucket_name):#Blob(binary large object): is a collection of binary data stored as a single entity
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return (f' succsessful')
    except Exception as e:
        print(e)
        return False

'''
Download Files
'''
def download_file_from_bucket(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        with open(file_path,'wb') as f:
            storage_client.download_blob_to_file(blob, f)
        return (f' succsessful')
    except Exception as e:
        print(e)
        return False

bucket_name = 'data_henry_pf'
download_file_from_bucket('Automotive', os.path.join(os.getcwd(),'file1.json'),bucket_name)