from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import pandas as pd
from datetime import datetime

import helper

# URL base
base_url = 'http://127.0.0.1:8000'

def get_url(path):
    return urljoin(base_url, path)

def process_country_page(url):
    try:
        country_response = requests.get(url)
        country_soup = BeautifulSoup(country_response.text, 'html.parser')
        
        tr_element = country_soup.find('tr', id='places_country__row')
        country = tr_element.find('td', class_='w2p_fw').text if tr_element else 'N/A'
        
        tr_element = country_soup.find('tr', id='places_currency_name__row')
        currency = tr_element.find('td', class_='w2p_fw').text if tr_element else 'N/A'
        
        tr_element = country_soup.find('tr', id='places_continent__row')
        continent = tr_element.find('td', class_='w2p_fw').text if tr_element else 'N/A'
        
        tr_element = country_soup.find('tr', id='places_neighbours__row')
        
        neighbours = helper.get_neighbours(tr_element)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Adiciona os dados à lista
        data.append({
            'País': country,
            'Moeda': currency,
            'Continente': continent,
            'Vizinhos': neighbours, # Nomes completos dos vizinhos.
            'Timestamp': timestamp
        })
    
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")

# Lista para armazenar os dados
data = []

# Coletar todas as páginas de países
country_pages = helper.get_all_country_pages()

# Processar cada página de país
for country_page in country_pages:
    print(f"Processando {country_page}")
    process_country_page(country_page)

# Converter a lista em um DataFrame do pandas
df = pd.DataFrame(data)

# Salvar o DataFrame em um arquivo CSV
df.to_csv('dados_paises.csv', index=False, encoding='utf-8')
print("Dados salvos com sucesso em 'dados_paises.csv'")
