# 🚀 Briefing Bot

Um robô para gerar um **briefing diário** com base em **notícias relevantes**, diretamente a partir de uma lista de URLs pré-definidas.  
Realiza o **scraping** e gera um arquivo final em **Markdown** — tudo automaticamente.

---

## Disclaimer
Projeto 100% criado utilizando ferramentas de IA para estudo de produtividade. Ferramentas utilizadas até o momento:
- Manus - estrutura do projeto
- Cursor - Refinamento do código, README, Docker
- GitHub Copilot - Autocomplete e correções
- Qodo - Criação dos testes unitários

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
|-- main.py              # Arquivo principal do projeto
|-- scrapers/            # Módulos de scraping para diferentes fontes
|    |-- pcl.py         # Scraper para PCL
|    |-- sal.py         # Scraper para SAL
|-- utils/              # Utilitários e funções auxiliares
|    |-- keywords.py    # Gerenciamento de palavras-chave
|    |-- md.py          # Formatação de Markdown
|    |-- db.py          # Operações com banco de dados
|-- configs/            # Arquivos de configuração
|    |-- urls.json      # URLs das fontes de notícias
|    |-- keywords.txt   # Palavras-chave para filtragem
|-- db/                 # Diretório para armazenamento do banco de dados
|-- briefings/          # Pasta com os briefings diários
|    |-- YYYY-MM-DD-briefing.md
|-- requirements.txt    # Dependências do projeto
|-- Dockerfile          # Configuração do container Docker
|-- docker-compose.yml  # Configuração do ambiente Docker
|-- README.md           # Documentação do projeto
|-- .gitignore          # Arquivos ignorados pelo Git
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

1. Certifique-se de ter o Docker e o Docker Compose instalados.
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

### Containers Órfãos

Durante o desenvolvimento, você pode encontrar avisos sobre "containers órfãos". Estes são containers que foram criados anteriormente, mas não estão definidos no seu arquivo `docker-compose.yml`. Para limpar estes containers, você pode usar:

```bash
docker-compose up --remove-orphans
```

Este comando irá:
1. Remover todos os containers órfãos.
2. Iniciar os serviços definidos no `docker-compose.yml`.

### Execução Local (Sem Docker)

Clone o repositório ou organize as pastas manualmente.

Crie e ative o ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

Execute o projeto:
```bash
python main.py
```

## 🧪 Testes

O projeto inclui testes unitários que podem ser executados usando Docker ou localmente.

### Usando Docker (Recomendado)

Para executar todos os testes:
```bash
docker-compose run test
```

Para executar um teste específico:
```bash
docker-compose run test pytest tests/test_pcl.py::test_scrape_all_new_pages_with_keywords -v
```

Para ver mais detalhes durante a execução dos testes:
```bash
docker-compose run test pytest tests/ -v -s
```

### Execução Local dos Testes

Com o ambiente virtual ativado, execute:
```bash
pytest tests/ -v
```

## 📝 Briefings

Os briefings são gerados automaticamente na pasta `briefings/` com o seguinte padrão de nome:
- `YYYY-MM-DD-briefing.md` (exemplo: `2024-03-21-briefing.md`)

Cada arquivo contém:
- Data e hora de geração
- Título da notícia
- URL da fonte
- Resumo do conteúdo

Todos os briefings do mesmo dia são salvos no mesmo arquivo, facilitando a leitura e organização do conteúdo.

## 📦 Dependências
- requests
- beautifulsoup4

## 💬 Contribuição
Sugestões, melhorias ou integrações são bem-vindas!

Crie um fork, abra um PR ou envie uma ideia.

