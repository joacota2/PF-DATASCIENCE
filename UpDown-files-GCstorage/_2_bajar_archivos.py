import requests
import _3_strings
import os

# Contar archivos en un directorio: https://pynative.com/python-count-number-of-files-in-a-directory/
def num_files():
    dir_path = r'./Datasets/'
    count = 0
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return(count)

# Bajar archivos de una url: https://www.codingem.com/python-download-file-from-url/
def bajar_primerosArchivos():
    for i in range(len(_3_strings.urls)):
        URL = _3_strings.urls[i]
        response = requests.get(URL)
        open("./Datasets/{}.json.gz".format(_3_strings.filenames[i]), "wb").write(response.content) 

# Bajar archivos de una url: https://www.codingem.com/python-download-file-from-url/
def bajar_nuevo_archivo(url):
    response = requests.get(url)
    n=num_files()+1
    open("./Datasets/file{}.json.gz".format(n), "wb").write(response.content)