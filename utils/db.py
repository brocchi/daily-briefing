# utils/db.py
import os

def should_scrape(url_target, file_name="db/scrapped.txt"):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    
    # If file doesn't exist, create it and return True (should scrape)
    if not os.path.exists(file_name):
        return True
        
    with open(file_name, 'r') as file:
        lines = [line.strip() for line in file]

    # Verificar se alguma line da lista está contida na string alvo
    match = any(line in url_target for line in lines)

    return not match # invert match value 


def summarize(html_text):
    return html_text[:300]  # Reduz para 300 caracteres


def save_scrapped(url, file_name="db/scrapped.txt"):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    
    with open(file_name, 'a', encoding='utf-8') as f:
        f.write(f"{url}\n")  # Adiciona a URL em negrito