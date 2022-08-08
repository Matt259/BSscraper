from bs4 import BeautifulSoup
import requests
import os
import pefile
import hashlib

headers ={"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}

def get_soft_paths():  # get each individual softwares path
    soft_paths = []
    index = 1
    while True:
        html = requests.get('https://sourceforge.net/directory/os:windows/?sort=popular&page= ' + str(index), headers=headers)
        soup = BeautifulSoup(html.text, 'html.parser')
        for path in soup.find_all('a' , class_ = 'button green hollow see-project'):
            if len(soft_paths) == 30:               
                return soft_paths
            else:
                path = path.get('href', None)
                soft_paths.append(path)       
        index = index + 1  
    
def get_download_paths():  # Gets the download path for each individual software
    download_paths = []
    for path in software_paths: 
        html = requests.get('https://sourceforge.net' + path, headers = headers)
        soup = BeautifulSoup(html.text, 'html.parser')
        download_btn = soup.find('a', class_='button download big-text green')
        pathz = download_btn.get('href', None)
        download_paths.append(pathz)    
    return download_paths

def get_download_links():  # List of all the download links for all the software
    download_links = []
    for download_path in download_paths:
        html = requests.get('https://sourceforge.net' + download_path, headers = headers)
        soup = BeautifulSoup(html.text, 'html.parser')
        meta_url = soup.find('meta', attrs={'http-equiv': 'refresh'})
        download_url = meta_url['content'].split('url=')[-1]
        download_links.append(download_url)   
    return download_links    

def download_files():  # Downloads each file off those links
    for link in download_links:
        path = link.split('/')[-1].split('?')[0]
        r = requests.get(link, stream=True)
        if r.status_code == 200:
            with open(r"Downloads/" + path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)

def remove_non_pe():  # Removes non PE files
    path = r"Downloads/"
    files = os.listdir(path)
    for file in files:
        path_and_file = path + file
        try:    
            pe = pefile.PE(path_and_file)
            magic = hex(pe.DOS_HEADER.e_magic)
            sig = hex(pe.NT_HEADERS.Signature)
        except:
            os.remove(path_and_file)

def to_sha1():  # Convert names to their SHA-1 values
    BLOCK_SIZE = 65536
    path = r"Downloads/"
    files = os.listdir(path)
    for file in files:
        path_and_file = path + file
        file_hash = hashlib.sha1()  # Create the hash object
        with open(path_and_file, 'rb') as f:  # Open the file to read it's bytes
            fb = f.read(BLOCK_SIZE)  # Read from the file. Take in the amount declared above
            while len(fb) > 0:  # While there is still data being read from the file
                file_hash.update(fb)  # Update the hash
                fb = f.read(BLOCK_SIZE)  # Read the next block from the file
        os.rename(path_and_file, path + file_hash.hexdigest())  # Rename the file


                 
if __name__ == '__main__': 
    #pass
    software_paths = get_soft_paths()
    download_paths = get_download_paths()
    download_links = get_download_links()
    #download_files()
    for link in download_links:
        print(link)
    #remove_non_pe()

    #to_sha1()






