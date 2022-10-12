import requests
import _3_strings
import os

# Contar archivos en un directorio: https://pynative.com/python-count-number-of-files-in-a-directory/
def num_files():
    dir_path = r'./Datasets/'
    count = 0
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    #print('File count:', count, type(count))
    return(count)

# Bajar archivos de una url: https://www.codingem.com/python-download-file-from-url/
def bajar_primerosArchivos():
    for i in range(len(_3_strings.urls)):
        URL = _3_strings.urls[i]
        response = requests.get(URL)
        # formatear una string: format: https://www.w3schools.com/python/trypython.asp?filename=demo_ref_string_format2
        open("./Datasets/{}.json.gz".format(_3_strings.filenames[i]), "wb").write(response.content) 

# Bajar archivos de una url: https://www.codingem.com/python-download-file-from-url/
def bajar_nuevo_archivo(url):
    response = requests.get(url)
    n=num_files()+1
    open("./Datasets/file{}.json.gz".format(n), "wb").write(response.content)