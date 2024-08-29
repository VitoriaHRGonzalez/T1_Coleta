from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin

# Faça um crawler capaz de navegar por todas as páginas de países e acessar seus HTML.
base_url = 'http://127.0.0.1:8000/places/default/index/'

def process_page(url):
    try:
        html = urlopen(url)
        bs = BeautifulSoup(html, 'html.parser')
        
        for link in bs.find_all('a'):
            if 'href' in link.attrs:
                full_url = urljoin(base_url, link.attrs['href'])
                print(f"Acessando: {full_url}")
                
                try:
                    link_html = urlopen(full_url)
                    link_bs = BeautifulSoup(link_html, 'html.parser')
                    print(link_bs.prettify())
                    
                except Exception as e:
                    print(f"Erro ao acessar {full_url}: {e}")
    
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")

for i in range(26):
    url = f"{base_url}{i}"
    print(f"Processando página: {url}")
    process_page(url)
