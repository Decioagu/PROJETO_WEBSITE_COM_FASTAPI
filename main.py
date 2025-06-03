from fastapi import FastAPI
from fastapi.middleware import Middleware # Importando o FastAPI e Middleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware # Middleware para validar o host
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware # Middleware para redirecionar para HTTPS

import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__)))) # caminho absoluto do diretório
from views import home_view, error_view 
from views.admin import admin_view 

middlewares = [
    Middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["localhost", "127.0.0.1"] # Hosts permitidos
    ),
    # Middleware(HTTPSRedirectMiddleware),
]

app = FastAPI(docs_url=None, 
              redoc_url=None, 
              exception_handlers=error_view.exception_handlers,
              middleware=middlewares) # Personalização de tratamento de erros

# ================================ ACESSO AS ROTAS ====================================
app.include_router(home_view.router) ###
app.include_router(admin_view.router) ###

# ================================ CAMINHO DA URL ====================================
from fastapi.staticfiles import StaticFiles
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # caminho absoluto
# print(f'main.py >>> {BASE_DIR}')

# Arquivos estáticos da pasta "Aula_28/static"
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
# Arquivos estáticos da pasta "Aula_28/media"
app.mount('/media', StaticFiles(directory=os.path.join(BASE_DIR, 'media')), name='media')
# ===================================================================================

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, log_level='info', reload=True)

# uvicorn main:app --reload

'''
Observação, o uso de "sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))",
consistem em adicionar o caminho absoluto do diretório atual ao sys.path:

OBS :
    Ao executar "uvicorn PROJETO_WEBSITE_COM_FASTAPI\main.py.main:app --reload",
    fora da pagina do projeto 

    Caso execute o "uvicorn main:app --reload" dentro da pasta Aula_20 utilize
    "templates = Jinja2Templates(directory='templates')" ou o arquivo não será encontrado.

REPOSITORIO/
├── PROJETO_WEBSITE_COM_FASTAPI/
│   └── main.py
│   templates/
│   └── index.html
│   └── servico.html 
'''
