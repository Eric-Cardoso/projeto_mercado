# 🛒 Projeto Mercado API

## Descrição

API REST de um sistema de mercado desenvolvida com FastAPI, utilizando autenticação com JWT, banco de dados SQLite e ORM com SQLAlchemy. Permite gerenciamento de usuários, produtos e carrinho de compras.

---

## Instruções de instalação

```bash
# Clonar o repositório
git clone https://github.com/Eric-Cardoso/projeto_mercado.git

# Acessar a pasta do projeto
cd projeto_mercado

# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate

# Linux / WSL / macOS
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

---

## Instruções de uso

```bash
# Rodar as migrations (na raiz do projeto)
alembic upgrade head

# Acessar a pasta src
cd src

# Iniciar o servidor
fastapi dev app.py
```

Acesse a documentação interativa no navegador:

```
http://127.0.0.1:8000/docs
```

Faça login pelo Swagger e utilize as rotas protegidas normalmente.

---

## 📖 Documentação (MkDocs)

> Certifique-se de ter instalado as dependências com `pip install -r requirements.txt`

### Rodar a documentação localmente

```bash
mkdocs serve -a 127.0.0.1:8001
```

Acesse a documentação no navegador:  
http://127.0.0.1:8001
