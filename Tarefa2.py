#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import json

# Considerando o site https://www.imdb.com/.
# 1) Faça scraping para obter os filmes presentes no Calendário de Lançamentos do IMDB.
# Devem ser obtidos: Título, Data de Lançamento, Gênero(s) e o link para página da série


def get_movies():
    base_url = "https://www.imdb.com/calendar/?ref_=rlm&region=BR"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }

    response = requests.get(base_url, headers=headers)
    bs = BeautifulSoup(response.text, "html.parser")
    articles = bs.find_all("article", class_="fyabhQ")
    filmes = []

    for a in articles:
        date = a.find("h3", class_="ipc-title__text").text
        for div in a.find_all("div", class_="ipc-metadata-list-summary-item__tc"):
            title = div.find("a", class_="ipc-metadata-list-summary-item__t").text
            genres = div.find("ul", class_="ipc-metadata-list-summary-item__tl")

            if genres:
                genre_list = [li.text for li in genres.find_all("li")]
                genre_text = ", ".join(genre_list)
            else:
                genre_text = "Não Contém"

            link = "https://www.imdb.com{}".format(
                div.find("a", class_="ipc-metadata-list-summary-item__t")["href"]
            )

            filmes.append(
                {"title": title, "date": date, "genres": genre_text, "link": link}
            )

    return filmes


# 2) Faça scraping das páginas específicas dos filmes obtidos no item anterior. Obtenha
# dessa página o(s) nome(s) do(s) diretor(es) e a lista dos atores presentes no elenco principal
# (Não é a lista completa de atores!)


def get_movie_details(filme):
    """Recebe um dicionário chamado filme, contendo o link para a página do filme e retorna o dicionário
    com os dados dos diretores e dos atores principais em um arquivo JSON."""

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    response = requests.get(filme["link"], headers=headers)
    bs = BeautifulSoup(response.text, "html.parser")

    # Diretores
    directors = []
    director_section = bs.find_all(
        "li",
        attrs={
            "role": "presentation",
            "class": "ipc-metadata-list__item",
        },  # busca todos os elementos <li> com o papel 'presentation' e classe 'ipc-metadata-list__item'
    )
    for section in director_section:
        label = section.find("span", class_="ipc-metadata-list-item__label")
        if label and "Director" in label.text:  # vai ate o nome do diretor
            director_names = section.find_all(
                "a", class_="ipc-metadata-list-item__list-content-item--link"
            )
            directors = [a.text.strip() for a in director_names]
            break

    # Elenco Principal ("Top Cast")
    main_cast = []
    actor_elements = bs.find_all(
        "a",
        attrs={
            "data-testid": "title-cast-item__actor"
        },  # busca todos os elementos <a> no HTML que possuem o atributo data-testid='title-cast-item__actor'
    )
    for actor in actor_elements:
        main_cast.append(
            actor.text.strip()
        )  # adiciona o nome do ator à lista após remover espaços em branco

    # Adiciona ao dicionário do filme
    filme["director(s)"] = directors
    filme["main cast"] = main_cast
    return filme


# 3) Salve as informações obtidas em um arquivo de tipo JSON
def save_to_json(filmes, filename="filmes_imdb.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(filmes, f, ensure_ascii=False, indent=4)


# main
if __name__ == "__main__":
    filmes = get_movies()

    for f in filmes:
        print(f"Título: {f['title']}\nData de Lançamento: {f['date']}\nGênero(s): {f['genres']}\nLink: {f['link']}\n\n")

    # Obter detalhes para cada filme e salvar em JSON
    for filme in filmes:
        filme = get_movie_details(filme)

    save_to_json(filmes)
