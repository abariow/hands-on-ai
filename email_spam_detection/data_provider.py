import os
import tarfile
import requests
from bs4 import BeautifulSoup

DATA_SOURCE_URL = 'https://spamassassin.apache.org/old/publiccorpus/'
DATA_PATH = 'data/'

# Reading data source page
response = requests.get(DATA_SOURCE_URL)
soup = BeautifulSoup(response.content, 'html5lib')

# Getting all data files names
download_links = soup.findAll('a', href=True)
data_files_names = [
    link['href'] for link in download_links if link['href'].endswith('.bz2')]

# Creating data directory
if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)

# Downloading data files
for file_name in data_files_names:
    if os.path.exists(DATA_PATH + file_name) \
        or os.path.exists(DATA_PATH + file_name.replace('.tar.bz2', '')):
        print('File already exists', file_name)
        continue
    print('Downloading', file_name)
    response = requests.get(DATA_SOURCE_URL + file_name)
    with open(DATA_PATH + file_name, 'wb') as f:
        f.write(response.content)

# Unzip data files
for file_name in data_files_names:
    if os.path.exists(DATA_PATH + file_name.replace('.tar.bz2', '')):
        print('File already unzipped', file_name)
        continue
    print('Unzipping', file_name)
    with tarfile.open(DATA_PATH + file_name, 'r:bz2') as f:
        f.extractall(DATA_PATH + file_name.replace('.tar.bz2', ''))
        
# Removing unziped data files
for file_name in data_files_names:
    print('Removing', file_name)
    os.remove(DATA_PATH + file_name)
