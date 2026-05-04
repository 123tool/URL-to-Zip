import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def fetch_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def download_assets(soup, base_url, folder_name):
    assets_path = os.path.join(folder_name, "assets")
    if not os.path.exists(assets_path):
        os.makedirs(assets_path)

    # Konfigurasi tag dan atribut yang dicari
    tags_config = {
        'img': 'src',
        'link': 'href',
        'script': 'src'
    }

    for tag, attr in tags_config.items():
        for element in soup.find_all(tag):
            asset_url = element.get(attr)
            if not asset_url or asset_url.startswith('data:'):
                continue

            full_url = urljoin(base_url, asset_url)
            file_name = os.path.basename(urlparse(full_url).path)
            
            # Jika file_name kosong (misal link ke direktori), lewati
            if not file_name:
                continue

            try:
                r = requests.get(full_url, stream=True, timeout=10)
                if r.status_code == 200:
                    local_file_path = os.path.join(assets_path, file_name)
                    with open(local_file_path, 'wb') as f:
                        for chunk in r.iter_content(1024):
                            f.write(chunk)
                    
                    # Update HTML agar mengarah ke folder assets lokal
                    element[attr] = f"assets/{file_name}"
            except:
                continue
    
    return soup
