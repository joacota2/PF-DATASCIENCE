#pip install --upgrade google-cloud-storage

import os
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ServiceKey_GoogleCloud.json'

storage_client = storage.Client()

'''
Create a New Bucket
'''
bucket_name = 'data_henry_pf'
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
my_bucket = storage_client.get_bucket('data_henry_pf')

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
file_path = r'C:\Users\marco\OneDrive\Desktop\API Google Cloud\Datasets'
Name = 'Automotive'
fileName = '18_Automotive.json'
bucket_name = 'data_henry_pf'
upload_to_bucket(Name, os.path.join(file_path,fileName),bucket_name)
#upload_to_bucket('/documents/Automotive', os.path.join(file_path,'18_Automotive_5.json'),'data_henry_pf')
'''

file_path = r'C:\Users\marco\OneDrive\Desktop\API Google Cloud\Datasets'
cloudnames_list = ['Home&Kitchen','KindleStore','Sports&Outdoors',
'Cellphones&Accessories','Health&PersonalCare','Toys&Games','VideoGames',
'Tools&HomeImprovement','Beauty','AndroidApps','Office','PetSupplies','Automotive',
'Grocery&GourmetFood','PatioLawn&Gard','Baby','DigitalMusic','MusicalInstruments',
'AmazonInstantVideo','Books','Electronics','Movies&TV','CD&Vinyl',
'Clothing&Shoes&Jewerly']
filenames_list = [
'6_Home_and_Kitchen.json','7_Kindle_Store.json','8_Sports_and_Outdoors.json',
'9_Cell_Phones_and_Accessories.json','10_Health_and_Personal_Care.json',
'11_Toys_and_Games.json','12_Video_Games.json','13_Tools_and_Home_Improvement.json',
'14_Beauty.json','15_Apps_for_Android.json','16_Office_Products.json','17_Pet_Supplies.json',
'18_Automotive.json','19_Grocery_and_Gourmet_Food.json','20_Patio_Lawn_and_Garden.json',
'21_Baby.json','22_Digital_Music.json','23_Musical_Instruments.json',
'24_Amazon_Instant_Video.json','1_Books.json','2_Electronics.json','3_Movies_and_TV.json',
'4_CDs_and_Vinyl.json','5_Clothing_Shoes_and_Jewelry.json']
print(len(filenames_list),len(cloudnames_list))
bucket_name = 'data_henry_pf'

for i in range(len(filenames_list)):
    upload_to_bucket(cloudnames_list[i], os.path.join(file_path,filenames_list[i]),bucket_name)
    print(f'archivo Nº {filenames_list[i]} subido')

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