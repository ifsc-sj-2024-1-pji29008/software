# Em construção

## Descrição

Este projeto é uma aplicação web que simula um sistema de monitoramento de sensores de temperatura e umidade. A aplicação é construída com Flask, um framework web leve e modular para Python.

## Funcionalidades

- **Listagem de Sensores**: Visualize todos os sensores cadastrados.
- **Detalhes do Sensor**: Veja informações detalhadas de um sensor específico.
- **Tipos de Sensores**: Veja o tipo de dispositivo que está sendo utilizado.

## Tecnologias

- **Flask**: Um framework web leve e modular para Python.
- **SQLite**: Um sistema de gerenciamento de banco de dados relacional.
- **Jinja2**: Um mecanismo de template para Python.
- **Gunicorn**: Um servidor HTTP WSGI para Python.
- **Nginx**: Um servidor web de código aberto.
- **Supervisor**: Um sistema de controle de processos para sistemas operacionais Unix.

## Requisitos

- Python 3.9+

## Configuração do Ambiente de Desenvolvimento

Utilizando um sistema operacional baseado em Unix (Linux ou macOS), siga as instruções abaixo para configurar o ambiente de desenvolvimento.

### Clonar o repositório

```bash
git clone -b 0.0.1 https://github.com/ifsc-sj-2024-1-pji29008/software.git
```

### Criar um ambiente virtual e instalar as dependências

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configurar as variáveis de ambiente

```bash
export FLASK_APP=run.py
export FLASK_ENV=development
```

### Iniciar a aplicação

```bash
./run.py
```

## Estrutura do Projeto

```
project_root/
│
├── app/
│   ├── __init__.py         # Cria e configura a aplicação Flask
│   ├── api.py              # Define os recursos da API (endpoints)
│   ├── routes.py           # Define as rotas da aplicação (endpoints)
│   ├── models.py           # Define os modelos de dados (usados com SQLAlchemy)
│   ├── database.py         # Inicializa e configura o banco de dados (SQLAlchemy)
│   ├── config.py           # Configurações da aplicação (variáveis de configuração)
│   ├── templates/          # Diretório para armazenar templates HTML
│   └── static/             # Diretório para arquivos estáticos (CSS, JS, imagens)
│
├── venv/                    # Ambiente virtual Python (não incluído no controle de versão)
│
├── logs/                    # Diretório para armazenar arquivos de log (não incluído no controle de versão)
│
├── config/                  # Diretório para configurações de implantação
│   ├── gunicorn_config.py   # Configurações do Gunicorn para execução do Flask
│   ├── nginx.conf           # Configurações do Nginx para servir o Flask via HTTP
│   └── supervisor.conf      # Configurações do Supervisor para gerenciar o processo do Flask
│
├── scripts/                 # Diretório para scripts utilitários
│   └── start_gunicorn.sh    # Script para iniciar o servidor Gunicorn
│
├── tests/                   # Diretório para testes da aplicação
│   ├── __init__.py
│   ├── test_app.py          # Testes unitários e de integração da aplicação Flask
│
├── requirements.txt         # Arquivo contendo todas as dependências do projeto
├── README.md                # Arquivo README com informações sobre o projeto
└── run.py                   # Script para iniciar a aplicação Flask em modo de desenvolvimento
