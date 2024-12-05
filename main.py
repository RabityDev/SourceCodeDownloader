import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def download_file(url, folder):
    local_filename = os.path.join(folder, os.path.basename(urlparse(url).path))
    
    
    if os.path.exists(local_filename):
        return local_filename
    
    
    response = requests.get(url)
    
    
    if response.status_code == 200:
        with open(local_filename, 'wb') as f:
            f.write(response.content)
    
    return local_filename


def modify_and_download(url, folder="downloaded_site"):
    
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return

    html_content = response.text
    
    
    soup = BeautifulSoup(html_content, 'html.parser')

    for img_tag in soup.find_all('img'):
        src = img_tag.get('src')
        if src:
            local_img = download_file(urljoin(url, src), folder)
            img_tag['src'] = os.path.basename(local_img)

    for link_tag in soup.find_all('link', {'rel': 'stylesheet'}):
        href = link_tag.get('href')
        if href:
            local_css = download_file(urljoin(url, href), folder)
            link_tag['href'] = os.path.basename(local_css)

    for script_tag in soup.find_all('script', {'src': True}):
        src = script_tag.get('src')
        if src:
            local_js = download_file(urljoin(url, src), folder)
            script_tag['src'] = os.path.basename(local_js)

   
    for a_tag in soup.find_all('a', href=True):
        href = a_tag.get('href')
        if not href.startswith('http') and not href.startswith('mailto'):
            local_link = os.path.basename(download_file(urljoin(url, href), folder))
            a_tag['href'] = local_link

    
    with open(os.path.join(folder, "index.html"), 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"Website downloaded and saved to {folder}/index.html")


site_url = 'SIteUrl'  
modify_and_download(site_url, folder="GitHub")
