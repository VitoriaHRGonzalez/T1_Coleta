from datetime import datetime
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import helper
import pandas as pd


# Verifica se houve atualização do país no .csv
def there_is_update(data, country, currency, continent, neighbours):
    data_country = data.loc[data[u'País'] == country]

    data_currency = data_country[u'Moeda'].values[0]
    data_continent = data_country[u'Continente'].values[0]
    data_neighbours = data_country[u'Vizinhos'].values[0]

    if data_currency == currency and data_continent == continent and data_neighbours == neighbours:
        return False
    return True


def get_country_info_from_page(bs):
    # Coletar as informações do país do HTML
    country = bs.find('tr', id='places_country__row').find('td', class_='w2p_fw').text  
    currency = bs.find('tr', id='places_currency_name__row').find('td', class_='w2p_fw').text
    continent = bs.find('tr', id='places_continent__row').find('td', class_='w2p_fw').text
    neighbours = helper.get_neighbours(bs.find('tr', id='places_neighbours__row'))
    return country, currency, continent, neighbours

def add_country(data, country, currency, continent, neighbours, file):
    print(f'Adicionando {country}')
    # Adiciona uma nova linha ao DataFrame
    new_row = pd.DataFrame({
        u'País': [country],
        'Moeda': [currency],
        'Continente': [continent],
        'Vizinhos': [neighbours],
        'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    })
    data = pd.concat([data, new_row], ignore_index=True)
    
    # Ordena as informações por país
    data = data.sort_values(by=u'País')

    # Salvar os dados no arquivo
    data.to_csv(file, sep=',', encoding='utf-8', index=False)

def update_country(data, country, currency, continent, neighbours, file):
    print(f'Atualizando {country} {currency} {continent} {neighbours}')
    # Atualiza as informações já existentes
    data.loc[data[u'País'] == country, 'Moeda'] = currency
    data.loc[data[u'País'] == country, 'Continente'] = continent
    data.loc[data[u'País'] == country, 'Vizinhos'] = neighbours
    data.loc[data[u'País'] == country, 'Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Salvar o DataFrame no arquivo CSV
    data.to_csv(file, sep=',', encoding='utf-8', index=False)
    
# Faça um crawler que monitore as páginas de países e procure por atualizações.
# Caso algum registro tenha sido atualizado desde sua obtenção, esse registro deve ser atualizado
# no arquivo CSV, caso contrário manter a versão anterior.
def check_update(): 
    # Coletar todas as páginas de países
    pages = helper.get_all_country_pages()

    # Ler o arquivo CSV
    file = 'dados_paises.csv'
    data = pd.read_csv(file, encoding='utf-8', keep_default_na=False)

    # Para cada página de país, coletar as informações e verificar se houve atualização
    for page in pages:
        response = requests.get(page)
        bs = BeautifulSoup(response.text, 'html.parser')

        # Coletar as informações no HTML
        country, currency, continent, neighbours = get_country_info_from_page(bs)

        print('Verificando {}'.format(country))

        # Adiciona país se não existir no .csv
        if country not in data[u'País'].values:
            add_country(data, country, currency, continent, neighbours, file)
        # Atualiza país se houver alteração
        elif there_is_update(data, country, currency, continent, neighbours):
            update_country(data, country, currency, continent, neighbours, file)

# Continua verificando atualizações enquanto o script estiver rodando
while True:
    check_update()