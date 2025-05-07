# utils/md.py
# Scrapper do tipo Parent-child-list

import re
import os
from datetime import datetime

def get_next_filename(base_dir="briefings"):
    """
    Gera o nome do arquivo de briefing baseado na data atual.
    Todos os briefings do mesmo dia serão salvos no mesmo arquivo.
    """
    # Cria o diretório se não existir
    os.makedirs(base_dir, exist_ok=True)
    
    # Formato do nome do arquivo: YYYY-MM-DD-briefing.md
    today = datetime.now().strftime('%Y-%m-%d')
    return os.path.join(base_dir, f"{today}-briefing.md")

def save_markdown(dados, nome_arquivo=None):
    """
    Salva o conteúdo em um arquivo markdown.
    Se nome_arquivo não for fornecido, usa o padrão de data.
    Todos os briefings do mesmo dia serão salvos no mesmo arquivo.
    """
    if nome_arquivo is None:
        nome_arquivo = get_next_filename()
    
    # Check if file exists to add header
    file_exists = os.path.exists(nome_arquivo)
    
    with open(nome_arquivo, 'a', encoding='utf-8') as f:
        # Add header if file is new
        if not file_exists:
            f.write("# Briefing Diário\n\n")
            f.write(f"*Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}*\n\n")
            f.write("---\n\n")
            
        f.write(f"## {clear_and_normalize(dados['title'])}\n")  # Adiciona título com formato de cabeçalho (H2)
        f.write(f"**URL:** {clear_and_normalize(dados['url'])}\n\n")  # Adiciona a URL em negrito
        f.write(f"**Resumo:** {clear_and_normalize(dados['summary'])}\n\n")  # Adiciona o resumo em negrito
        f.write("---\n")  # Linha de separação entre os itens

def clear_and_normalize(string):
    return re.sub(r'\s+', ' ', string).strip()
