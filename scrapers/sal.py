# scrapers/sal.py
# Scrapper do tipo Selector-Anchor-list

import utils.md
import utils.db
import utils.keywords
import requests
from bs4 import BeautifulSoup


def get_child_pages(target):

    print(target)

    # Requisição HTTP
    response = requests.get(target['url'], timeout=10)
    response.raise_for_status()  # Garante que a resposta foi 200

    # Parsear o HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Busca os elementos a serem coletados
    elementos = soup.css.select(target['anchor_selector'], limit=target['depth'])

    for elemento in elementos:
        url = f"{target['uri']}{elemento['href']}"
        if utils.db.should_scrape(url):
            scrape_page(url, target)


def scrape_page(url, target):
    # Log do tipo de scrapper e URL
    print(f"[INFO] Scrapper Type: Selector-Anchor-list | URL: {url}")

    # Requisição HTTP
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Garante que a resposta foi 200

    # Parsear o HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.css.select_one(target['page']['title']).get_text()
    content = soup.css.select_one(target['page']['content']).get_text()
    
    utils.db.save_scrapped(url)
    
    # Verifica se o conteúdo contém as palavras-chave
    has_keywords, required_words = utils.keywords.check_content_has_keywords(content)
    if not has_keywords:
        print(f"Página ignorada - não contém todas as palavras requeridas")
        return
    
    summary = utils.db.summarize(content)

    print(title)
    print("----------------------------------------------")


    # Salvar no arquivo markdown
    utils.md.save_markdown({"title":title,"url":url,"summary":summary})
