from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup


# Faça um crawler capaz de navegar por todas as páginas de países e acessar seus HTML.
base_url = 'http://127.0.0.1:8000/places/default/index'

html = urlopen(base_url)
bs = BeautifulSoup(html, 'html.parser')

for link in bs.find_all('a'):
    if 'href' in link.attrs:
        url = urljoin(base_url, link.attrs['href'])
        print(f"Acessando: {url}")
        
        try:
            link_html = urlopen(url)
            link_bs = BeautifulSoup(link_html, 'html.parser')
            
            print(link_bs.prettify())
        
        except Exception as e:
            print(f"Erro ao acessar {url}: {e}")


