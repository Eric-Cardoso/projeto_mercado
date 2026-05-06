# 🛒 Projeto Mercado API

## 📌 Descrição

API REST desenvolvida com FastAPI que simula um sistema de mercado.  
A aplicação permite autenticação de usuários, gerenciamento de produtos e controle de carrinho de compras.

O projeto segue uma arquitetura em camadas, separando responsabilidades entre rotas, serviços e acesso ao banco de dados.

---

## 🚀 Tecnologias utilizadas

- FastAPI
- SQLite
- SQLAlchemy
- JWT (autenticação)
- Bcrypt (hash de senha)
- Alembic (migrations)

---

## 🧱 Arquitetura do projeto

O projeto está organizado em camadas:

- **routers** → definição das rotas (endpoints)
- **services** → regras de negócio
- **repos** → acesso ao banco de dados
- **schemas** → validação de dados (Pydantic)
- **models** → estrutura das tabelas (SQLAlchemy)

---

## 🔐 Autenticação

A autenticação é feita utilizando JWT.

### Fluxo:

1. usuário envia email e senha
2. sistema valida credenciais
3. retorna:
   - access_token
   - refresh_token
4. rotas protegidas exigem usuário autenticado

Senhas são armazenadas de forma segura utilizando hash com Bcrypt.

---

## 👤 Usuários

Funcionalidades:

- criar usuário
- obter dados do usuário
- atualizar dados
- deletar usuário

### Regras:

- email deve ser único
- senha é validada antes de ser salva
- apenas admins podem acessar rotas administrativas

---

## 🛒 Carrinho

Funcionalidades:

- criar carrinho automaticamente ao adicionar produto
- listar carrinho
- cancelar compra
- finalizar compra

### Regras:

- cada usuário possui um carrinho
- carrinho possui status:
  - pendente
  - cancelado
  - finalizado
- calcula automaticamente:
  - total de produtos
  - valor total
  - desconto total

---

## 📦 Produtos

Funcionalidades:

- adicionar produto ao carrinho
- listar produtos
- buscar produto específico
- atualizar produto
- deletar produto

### Regras:

- produto pertence a um carrinho
- usuário só pode acessar seus próprios produtos
- descontos são aplicados automaticamente

---

## 💸 Sistema de descontos

Os descontos são aplicados automaticamente com base no dia da semana:

- segunda → refrigerados (20%)
- terça → hortifruti (50%)
- quarta → açougue (30%)
- quinta → padaria (40%)
- sexta → bebidas (50%)
- sábado → geral (20%)

O cálculo considera:
- preço unitário
- quantidade

---

## 📦 Instalação

```bash
# Clonar o repositório
git clone https://github.com/Eric-Cardoso/projeto_mercado.git

# Acessar a pasta do projeto
cd projeto_mercado

# Configurar variáveis de ambiente
cp .env-example .env
# preencher o .env com suas configurações

# Criar o ambiente virtual

# Linux / WSL / macOS
python3 -m venv venv

# Windows (PowerShell / CMD)
python -m venv venv
# ou
py -m venv venv

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

## ⚙️ Execução do projeto

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

## 📖 Documentação (MkDocs)

> Certifique-se de ter instalado as dependências com `pip install -r requirements.txt`

### Rodar a documentação localmente

```bash
mkdocs serve -a 127.0.0.1:8001
```

Acesse a documentação no navegador:  
http://127.0.0.1:8001

