# 🚀 Briefing Bot

Um robô para gerar um **briefing diário** com base em **notícias relevantes**, diretamente a partir de uma lista de URLs pré-definidas.  
Faz o **scraping** e gera um arquivo final em **Markdown** — tudo automaticamente.

-- 

## Disclamer
Projeto 100% criado utilizando ferramentas de IA para estudo de produtividade. Ferramentas utilizadas até o momento:
- Manus - estrutura do projeto
- Cursor - Refinamento do código, README, Docker

---

## 🎯 Objetivo do Projeto

Automatizar a coleta e organização de notícias importantes, ajudando você a **começar o dia informado** sem perder tempo com leitura irrelevante.

**Resumo das entregas:**
- Scraping seguro de notícias a partir de URLs
- Geração de briefing em Markdown
- Armazenamento em banco de dados

---

## 🏗 Estrutura do Projeto

```
/
|-- main.py
|-- scrapers/
|    |-- __init__.py
|    |-- scraper.py
|-- utils/
|    |-- __init__.py
|    |-- formatter.py
|-- configs/
|    |-- themes.json
|-- db/
|-- requirements.txt
|-- Dockerfile
|-- docker-compose.yml
|-- README.md
|-- conteudos.md
```

---

## ⚙️ Configurações Iniciais

1. **URLs de Notícias**

   Crie o arquivo `configs/urls.txt` com uma URL de notícia por linha, exemplo:

```
    https://g1.globo.com/economia/noticia/2025/04/25/banco-central-eleva-juros.ghtml 
    https://www.cnnbrasil.com.br/tecnologia/startup-brasileira-revoluciona-pagamentos/
```

## 🛠️ Execução do Projeto

### Usando Docker (Recomendado)

1. Certifique-se de ter o Docker e Docker Compose instalados
2. Execute o projeto:
```bash
docker-compose up --build
```

Para executar em segundo plano:
```bash
docker-compose up -d
```

Para parar o container:
```bash
docker-compose down
```

### Execução Local (Sem Docker)

Clone o repositório ou organize as pastas manualmente.

Crie e ative o ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # (Linux/macOS)
.\venv\Scripts\activate    # (Windows)
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

Execute o projeto:
```bash
python main.py
```

Resultado:
Um arquivo `conteudos.md` será gerado na raiz do projeto.

## 📦 Dependências
- requests
- beautifulsoup4

## 💬 Contribuição
Sugestões, melhorias ou integrações são bem-vindas!

Crie um fork, abra um PR ou só mande uma ideia.

