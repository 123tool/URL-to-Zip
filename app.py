import os
from flask import Flask, render_template, request, send_file
from core.downloader import fetch_html, download_assets
from core.archiver import create_zip
from bs4 import BeautifulSoup
from urllib.parse import urlparse

app = Flask(__name__)

# Konfigurasi folder penyimpanan
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url or not url.startswith('http'):
            return "URL tidak valid!", 400

        # Penamaan folder berdasarkan domain agar unik
        domain = urlparse(url).netloc.replace('.', '_')
        folder_name = os.path.join(DOWNLOAD_DIR, f"cloned_{domain}")
        
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Proses Fetching & Cloning
        html_data = fetch_html(url)
        if "Error" in html_data:
            return f"Gagal kloning: {html_data}", 500
            
        soup = BeautifulSoup(html_data, 'html.parser')
        
        # Download aset (CSS, JS, Images) secara otomatis
        soup_final = download_assets(soup, url, folder_name)

        # Simpan file index.html
        index_file = os.path.join(folder_name, "index.html")
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(soup_final.prettify())

        # Kompres ke ZIP
        zip_filename = f"cloned_{domain}.zip"
        zip_path = os.path.join(DOWNLOAD_DIR, zip_filename)
        create_zip(folder_name, zip_path)

        return send_file(zip_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    print("Server berjalan di http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
