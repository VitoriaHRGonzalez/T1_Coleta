# Tarefa 1 – Web Scraping em Ambiente Controlado

- Crawler capaz de navegar por todas as páginas de países e acessar seus HTML 

- Scraping dos HTMLs das páginas para armazenar os seguintes dados em um arquivo CSV: 
  - Nome do país (campo country) → Country
  - Nome da moeda (campo currency name) → Currency Name
  - Nome do continente que pertence (campo continente) → Continent
  - Nome de todos os países vizinhos (campo neighbours - Atenção, é o NOME e não a sigla!) → Neighbours
  - Salvar uma coluna extra no csv contendo um timestamp do momento no qual os dados foram obtidos

- Crawler que monitore as páginas de países e procure por atualizações


# Tarefa 2 – Web Scraping em Ambiente Real

- Site: https://www.imdb.com/

- Scraping para obter os filmes presentes no Calendário de Lançamentos do IMDB. 
Obtenha o Título, Data de Lançamento, Gênero(s) e o link para página da série.

- Scraping das páginas específicas dos filmes obtidos no item anterior. 
Obtenha dessa página o(s) nome(s) do(s) diretor(es) e a lista dos atores presentes no elenco principal

- Salvar as informações obtidas em um arquivo de tipo JSON
