# ========================= CAMINHO ARQUIVO SQLite ==============================
from pathlib import Path # Pasta

# Criando uma engine para um banco SQLite (ou pode ser MySQL, PostgreSQL etc.)
caminho_do_arquivo = Path(__file__).parent.parent

# ======================= CONEXÃO BANCO DE DADOS ===============================
from sqlalchemy.ext.declarative import declarative_base
# Definição direta da URL do Banco de Dados
# DB_URL: str = 'mysql+aiomysql://root:Enigma.1@localhost:3306/novo_startup' # MySQL
DB_URL: str = f"sqlite+aiosqlite:///{caminho_do_arquivo}/novo_startup.db" # SQLite

DBBaseModel = declarative_base()

# ========================= SESSÃO BANCO DE DADOS =============================
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

# conexão do Banco de Dados (ENDEREÇO BANCO DE DADOS)
engine: AsyncEngine = create_async_engine(DB_URL, echo=False) 

# Cria sessão de Banco de Dados assíncrono (INTERAÇÃO)
Session: AsyncSession = sessionmaker(
    autocommit=False, # não faz "commit" automaticamente
    autoflush=False, # não executar consulta automáticas 
    expire_on_commit=False, # sessão não aspirá apos "commit"
    class_=AsyncSession, #  sessão assíncrono
    bind=engine # ativa conexão com o banco de dados
)
# ================= SESSÃO COMMIT (ABERTURA E FECHAMENTO) ======================
from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager ###

'''
@asynccontextmanager é um decorador que transforma uma função com async def e yield 
em um gerenciador de contexto assíncrono compatível com async with, quado não se utiliza
Depends() do FastAPI na funções. 

Exp:
    async def get(db: AsyncSession = Depends(get_session)):
    
Em FastAPI, o Depends() é usado para injeção de dependência juntamente com as rotas, uma técnica que 
permite reutilizar lógica comum (como autenticação, conexão com Banco de Dados, validação, etc.) 
em múltiplos endpoints de forma limpa e organizada.
'''

# Consulta no Banco de Dados
@asynccontextmanager ###
async def get_session() -> Generator:
    session: AsyncSession = Session()

    try:
        yield session # Abrir sessão
    finally:
        await session.close() # Fechar sessão
        
# ========================= ROTAS API (RECURSOS) ===============================
from fastapi.templating import Jinja2Templates
import os 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # caminho
# print(f'configs.py >>> {BASE_DIR}')
# Certifique-se de que o caminho está correto "Aula_26/templates"
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates")) 
# Certifique-se de que o caminho está correto "Aula_26/media"
media = os.path.join(BASE_DIR, "media") 

from typing import ClassVar
from pydantic_settings import BaseSettings
# Gerenciar configurações de aplicativos
class Settings(BaseSettings):

    TEMPLATES: ClassVar[Jinja2Templates] = templates  # anotação templates
    MEDIA: ClassVar[str] = media # anotação rota
    AUTH_COOKIE_NAME: str = "auth_cookie" # cookie de autenticação salvo no navegador HTML
    SALTY: str = 'AnyKwYandMA7o6Cz0MTksByXHriT2fRuAO2p-0y3SbhR3Ou1PnItPFX7zL3cXo861PA9ByalGBneR7O27QRvWw' # texto aleatório para criptografia

    class Config:
        case_sensitive = True

# Cria uma instância de conexão Banco de Dados
settings = Settings()
