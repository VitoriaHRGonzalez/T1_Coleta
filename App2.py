from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

# Faça scraping dos HTMLs das páginas para armazenar os seguintes dados dos países em um arquivo CSV:
# Nome do país, moeda, continente, vizinhos e timestamp da coleta.
base_url = 'http://127.0.0.1:8000/places/default/index'

response = requests.get(base_url)
bs = BeautifulSoup(response.text, 'html.parser')
data = []

for link in bs.find_all('a'):
    if 'href' in link.attrs:
        full_url = urljoin(base_url, link.attrs['href'])
        print(f"Acessando: {full_url}")
        
        try:
            country_response = requests.get(full_url)
            country_soup = BeautifulSoup(country_response.text, 'html.parser')
            
            tr_element = country_soup.find('tr', id='places_country__row')
            country = tr_element.find('td', class_='w2p_fw').text
            
            tr_element = country_soup.find('tr', id='places_currency_name__row')
            currency = tr_element.find('td', class_='w2p_fw').text
            
            tr_element = country_soup.find('tr', id='places_continent__row')
            continent = tr_element.find('td', class_='w2p_fw').text
            
            tr_element = country_soup.find('tr', id='places_neighbours__row')
            neighbours = tr_element.find('td', class_='w2p_fw').text
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Adiciona os dados à lista
            data.append({
                'País': country,
                'Moeda': currency,
                'Continente': continent,
                'Vizinhos': neighbours,
                'Timestamp': timestamp
            })
        
        except Exception as e:
            print(f"Erro ao acessar {full_url}: {e}")

# Converter a lista em um DataFrame do pandas
df = pd.DataFrame(data)

# Salvar o DataFrame em um arquivo CSV
df.to_csv('dados_paises.csv', index=False, encoding='utf-8')

print("Dados salvos com sucesso em 'dados_paises.csv'")
