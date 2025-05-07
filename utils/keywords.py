import os


def load_required_keywords():
    """
    Carrega as palavras-chave do arquivo de configuração.
    Retorna uma lista de palavras-chave em lowercase, ignorando comentários e linhas vazias.
    """
    keywords_file = os.path.join('configs', 'keywords.txt')
    if not os.path.exists(keywords_file):
        return []
    
    with open(keywords_file, 'r', encoding='utf-8') as f:
        # Ignora linhas de comentário e linhas vazias, e converte para lowercase
        keywords = [line.strip().lower() for line in f if line.strip() and not line.startswith('#')]
    return keywords


def check_content_has_keywords(content, required_words=None):
    """
    Verifica se o conteúdo contém pelo menos uma das palavras-chave requeridas.
    
    Args:
        content (str): O conteúdo a ser verificado
        required_words (list, optional): Lista de palavras-chave. Se None, carrega do arquivo.
    
    Returns:
        tuple: (bool, list) - (True se contém pelo menos uma palavra, lista de palavras requeridas)
    """
    if required_words is None:
        required_words = load_required_keywords()
    
    if not required_words:
        return True, []
    
    content_lower = content.lower()
    has_any_word = any(word.lower() in content_lower for word in required_words)
    return has_any_word, required_words 