import os
import sys
from core.downloader import fetch_html, download_assets
from core.archiver import create_zip
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from colorama import Fore, Style, init

init(autoreset=True)

def main():
    print(f"{Fore.YELLOW}{'='*45}")
    print(f"{Fore.CYAN}    SPY-E WEB CLONER - TERMINAL VERSION")
    print(f"{Fore.YELLOW}{'='*45}")
    
    url = input(f"{Fore.GREEN}[?] Masukkan URL Website: {Style.RESET_ALL}")
    if not url.startswith('http'):
        print(f"{Fore.RED}[!] URL Tidak Valid!")
        return

    domain = urlparse(url).netloc.replace('.', '_')
    output_dir = f"cloned_{domain}"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"{Fore.BLUE}[*] Sedang mengambil HTML...")
    content = fetch_html(url)
    
    print(f"{Fore.BLUE}[*] Mendownload file CSS, JS, dan Gambar...")
    soup = BeautifulSoup(content, 'html.parser')
    soup_final = download_assets(soup, url, output_dir)

    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(soup_final.prettify())

    print(f"{Fore.BLUE}[*] Membungkus file ke ZIP...")
    zip_path = f"{output_dir}.zip"
    create_zip(output_dir, zip_path)

    print(f"{Fore.GREEN}[SUCCESS] Kloning selesai!")
    print(f"{Fore.CYAN}[INFO] File ZIP: {zip_path}")

if __name__ == "__main__":
    main()
