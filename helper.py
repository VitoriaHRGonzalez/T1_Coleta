from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

# Script para coletar as páginas de países
base_url = 'http://127.0.0.1:8000'

def get_url(path):
    return urljoin(base_url, path)

def get_all_country_pages():
    has_next = True

    # pagina inicial
    current = requests.get(get_url('/places/default/index'))

    data = []

    while(has_next):
        # pega o conteúdo da página
        bs = BeautifulSoup(current.text, 'html.parser')

        # pega os links das páginas dos paises
        pages = [get_url(link['href']) for link in bs.find('table').find_all('a')]

        # pega o link para a próxima página
        next_element = bs.find('a', text='Next >')

        # adiciona os links na lista que será retornada
        data.extend(pages)

        # se houver próxima página, pega o link dela
        # se não, finaliza o while
        if next_element:
            current = requests.get(get_url(next_element['href']))
        else:
            has_next = False
    # retorna a lista de links
    return data

# Função para coletar os vizinhos de um país
def get_neighbours(tr_element):
    neighbours_list = []
    if tr_element:
        # pegar cara link de vizinho
        for link in tr_element.find('td', class_='w2p_fw').find_all('a'):
            neighbour_url = urljoin(base_url, link['href'])
            try:
                # acessar a página do vizinho
                neighbour_response = requests.get(neighbour_url)
                neighbour_response.encoding = 'utf-8'
                neighbour_soup = BeautifulSoup(neighbour_response.text, 'html.parser')
                
                # pegar o nome do vizinho
                neighbour_country_tr = neighbour_soup.find('tr', id='places_country__row')
                neighbour_country = neighbour_country_tr.find('td', class_='w2p_fw').text if neighbour_country_tr else u'Não contém'
                
                neighbours_list.append(neighbour_country)
            
            except Exception as e:
                print(u"Erro ao acessar o vizinho {}: {}".format(neighbour_url,e))
    # retornar a lista com os nomes dos vizinhos
    return u', '.join(neighbours_list) if neighbours_list else u'N/A'