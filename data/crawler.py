import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl_website(url, visited_urls=None):
    """
    Menelusuri tautan-tautan di dalam sebuah situs web.
    """
    if visited_urls is None:
        visited_urls = set()

    if url in visited_urls:
        return
    
    print(f"Mengunjungi: {url}")
    visited_urls.add(url)

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Temukan semua tautan (link)
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Gabungkan URL relatif dengan URL dasar
            absolute_url = urljoin(url, href)
            # Hanya telusuri tautan internal (domain yang sama)
            if absolute_url.startswith(url):
                crawl_website(absolute_url, visited_urls)

    except requests.exceptions.RequestException as e:
        print(f"❌ Error saat mengambil URL: {url} - {e}")

# Contoh penggunaan
starting_url = "https://dqlab.id/"
crawl_website(starting_url) # Aktifkan baris ini untuk menjalankan crawler