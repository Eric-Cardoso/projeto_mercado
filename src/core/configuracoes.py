from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# Carrega as variáves do .env
load_dotenv()

# Estabelece o banco que será utilizado e o nome do arquivo do banco
DATABASE_URL = 'sqlite:///mercado.db'

# Cria a engine
engine = create_engine(DATABASE_URL)
# Cria a sessão local através da engine
Sessionlocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
# Cria o Base
Base = declarative_base()

# Pega a SECRET_KEY do .env
CHAVE_SECRETA = os.getenv('CHAVE_SECRETA')
ALGORITMO = os.getenv('ALGORITMO')
TEMPO_EXPIRACAO_TOKEN = int(os.getenv('TEMPO_EXPIRACAO_TOKEN'))