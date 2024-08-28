#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from bs4 import BeautifulSoup
import requests

# Considerando o site https://www.imdb.com/.
# 1) Faça scraping para obter os filmes presentes no Calendário de Lançamentos do IMDB. 
# Devem ser obtidos: Título, Data de Lançamento, Gênero(s) e o link para página da série

base_url = 'https://www.imdb.com/calendar/?ref_=rlm&region=BR'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

response = requests.get(base_url, headers=headers)

bs = BeautifulSoup(response.text, 'html.parser')
articles = bs.find_all('article', class_='fyabhQ')

filmes = []

for a in articles:
    date = a.find('h3', class_='ipc-title__text').text
    for div in a.find_all('div', class_='ipc-metadata-list-summary-item__tc'):
        title = div.find('a', class_='ipc-metadata-list-summary-item__t').text
        genres = div.find('ul', class_='ipc-metadata-list-summary-item__tl')

        if genres:
            genre_list = [li.text for li in genres.find_all('li')]
            genre_text = ', '.join(genre_list)
        else:
            genre_text = 'N/A'

        link = 'https://www.imdb.com{}'.format(div.find('a', class_='ipc-metadata-list-summary-item__t')['href'])
        
        filmes.append({
            'title': title,
            'date': date,
            'genres': genre_text,
            'link': link
        })

for f in filmes:
    print(u'Título: {}\nData de Lançamento: {}\nGênero(s): {}\nLink: {}\n\n'.format(f['title'], f['date'], f['genres'], f['link']))
