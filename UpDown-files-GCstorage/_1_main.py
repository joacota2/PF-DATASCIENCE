import os

import _2_bajar_archivos
import _3_strings
import _4_GCS

# descarga los primeros archivos del repositorio
_2_bajar_archivos.bajar_primerosArchivos() 

# Subir los archivos a google cloud storage
file_path = './Datasets'
bucket_name = 'bucket-pf-henry'
filenames_list = _3_strings.filenames
cloudnames_list = _3_strings.cloudnames
for i in range(len(filenames_list)): #for i in range(-3,-2): 
    print(f'Subiendo archivo {filenames_list[i]} ...')
    _4_GCS.upload_to_bucket(cloudnames_list[i], os.path.join(file_path,filenames_list[i]+'.json.gz'),bucket_name)
    print(f'archivo {filenames_list[i]}.json.gzip subido')