# main.py

import json
import scrapers.pcl
import scrapers.sal

def load_urls(file_path):
    """Carrega a lista de URLs de um arquivo txt."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def default_exception(target):
    raise ValueError(f"Opção inválida: {target['type']}")


def main():
    # 1. Carregar URLs
    urls = load_urls('configs/urls.json')

    cases = {
        "pcl": scrapers.pcl.get_child_pages,
        "sal": scrapers.sal.get_child_pages
    }

    for target in urls['target']:
        func = cases.get(target['type'], default_exception)
        func(target)


if __name__ == "__main__":
    main()
