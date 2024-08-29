#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from urlparse import urljoin

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

