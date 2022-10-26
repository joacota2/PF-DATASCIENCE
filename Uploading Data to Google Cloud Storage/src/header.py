import gzip
import os
from google.cloud import storage
import pandas as pd
import csv

filenames = [
        'MusicalInstruments',
        'Automotive',
        'PatioLawnAndGard',
        'AmazonInstantVideo',
        'Office',
        'DigitalMusic',
        'PetSupplies',
        'GroceryAndGourmetFood',
        'ToolsAndHomeImprovement',
        'Baby',
        'ToysAndGames',
        'Beauty',
        'CellphonesAndAccessories',
        'ClothingAndShoesAndJewerly',
        'SportsAndOutdoors',
        'HealthAndPersonalCare',
        #'AndroidApps',
        'VideoGames',
        'HomeAndKitchen',
        #'KindleStore',
        'CDAndVinyl',
        'Electronics',
        'MoviesAndTV',
        'Books',
        #'Metadata'
                ]

urls =  [
        #Musical Instruments
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Musical_Instruments_5.json.gz',
        #Automotive
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Automotive_5.json.gz',
        #Patio, Lawn and Garden
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Patio_Lawn_and_Garden_5.json.gz',
        #Amazon Instant Video
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Amazon_Instant_Video_5.json.gz',
        #Office
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Office_Products_5.json.gz',
        #Digital Music
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Digital_Music_5.json.gz',
        #Pet Supplies
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Pet_Supplies_5.json.gz',
        #Grocery and Gourmet Food
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Grocery_and_Gourmet_Food_5.json.gz',
        #Tools and Home Improvement
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Tools_and_Home_Improvement_5.json.gz',
        #Baby
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Baby_5.json.gz',
        #Toys and Games
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Toys_and_Games_5.json.gz',
        #Beauty
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Beauty_5.json.gz',
        #Cell Phones and Accesories
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Cell_Phones_and_Accessories_5.json.gz',
        #Clothing, Shoes and Jewelry
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Clothing_Shoes_and_Jewelry_5.json.gz',
        #Sports and Outdoors
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Sports_and_Outdoors_5.json.gz',
        #Health and Personal Care
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Health_and_Personal_Care_5.json.gz',
        #Apps for Android
        #'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Apps_for_Android_5.json.gz',
        #Video Games
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Video_Games_5.json.gz',
        #Home and Kitchen
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Home_and_Kitchen_5.json.gz',
        #Kindle Store
        #'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Kindle_Store_5.json.gz',
        #CD and Vinyl
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_CDs_and_Vinyl_5.json.gz',
        #Electronics
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Electronics_5.json.gz', 
        #Movies and TV
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Movies_and_TV_5.json.gz',       
        #Books
        'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Books_5.json.gz',
        #Metadata
        #'http://snap.stanford.edu/data/amazon/productGraph/metadata.json.gz'
                ]

def parse(path):
    with gzip.open(path, 'rb') as g:
        for l in g:
            yield eval(l)

def save_partition(filename,df,chunksnum,type):
    dfout = pd.DataFrame.from_dict(df, orient='index')
    if type == '.csv':
        dfout.to_csv('./Datasets/CSVs/{}_{}{}'.format(filename.replace('.json.gz',''),chunksnum,type),index=False,sep=',')
    else: 
        dfout.to_json(path_or_buf='./Datasets/CSVs/{}_{}{}'.format(filename.replace('.json.gz',''),chunksnum,'.json'))
    return(True)

def getChunkDF(filepath,filename,chunklen,type='.csv'):
  '''
  Parámetros: 
  filepath: ruta de origen del archivo .gz
  filename: nombre del archivo en formato .gz
  chunklen: número de filas del fragmento
  type: tipo de archivo, .csv por defecto
  '''
  path = os.path.join(filepath,filename)
  i = 0
  df = {}
  chunksnum = 1
  for d in parse(path):
    df[i] = d
    i += 1
    if i == chunklen:
      save_partition(filename,df,chunksnum,type)
      df = {}; chunksnum += 1; i = 0 # Reinicia variables
  if i != 0: save_partition(filename,df,chunksnum,type)
  return True



os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './Credentials/GCS.json'
storage_client = storage.Client()

def create_bucket(bucket_name):
    bucket_name = 'bucket-pf-henry'
    bucket = storage_client.bucket(bucket_name)
    bucket.location = 'US'
    try:
        bucket = storage_client.create_bucket(bucket)
    except Exception as e:
        print (e)


def upload_to_bucket(blob_name,file_path,bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return(True)
    except Exception as e:
        print (e)
        return False

types = [str, str, str, str, str, float, str, int, str]

def ReplaceNulls(filepath,filename,fileFormat):
    path = os.path.join(filepath,filename)
    if fileFormat == '.csv':
        df = pd.read_csv(path)
    else:
        df = pd.read_json(path)
    for i in range(df.shape[1]):
        if (types[i] == str):
            df.iloc[:,i] = df.iloc[:,i].fillna('no data')
        elif (types[i] == float):
            df.iloc[:,i] = df.iloc[:,i].fillna(0.0)
        elif (types[i] == int):
            df.iloc[:,i] = df.iloc[:,i].fillna(0)
    if fileFormat == '.csv': 
        df.to_csv('./Datasets/ETL/{}'.format(filename),index=False)
    else: 
        df.to_json('./Datasets/ETL/{}'.format(filename))
    return(df)

def helpfulAndDate(filepath,filename):
    path = os.path.join(filepath,filename)
    df = pd.read_csv(path)
    new = df["helpful"].str.split(",", n = 1, expand = True)
    new[0]=new[0].str.replace(",","")
    new.loc[:,0]=new.loc[:,0].map(lambda x: x.replace('[',''))
    new.loc[:,1]=new.loc[:,1].map(lambda x: x.replace(']',''))
    df['UsefulReviews'] = new.loc[:,0]
    df['TotalReviews'] = new.loc[:,1]
    df.drop(columns =["helpful"], inplace = True)

    df["Date"] = pd.to_datetime(df['unixReviewTime'], unit='s')
    df.drop(columns =["reviewTime"], inplace = True)
    df['Date']=pd.to_datetime(df['Date'].astype(str), format='%Y/%m/%d')
    return (df)