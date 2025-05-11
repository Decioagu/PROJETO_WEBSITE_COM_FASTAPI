from fastapi import FastAPI

import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__)))) # caminho absoluto do diretório
from views import home_view, error_view
from views.admin import admin_view ###

app = FastAPI(docs_url=None, redoc_url=None, exception_handlers=error_view.exception_handlers) # elimina pagina de documentação FastAPI

# ================================ ACESSO AS ROTAS ====================================
app.include_router(home_view.router)
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
Execução:
    Fora da pasta: uvicorn Aula_28.main:app --reload
    Dentro da pasta: uvicorn main:app --reload

Paginas de navegação:
    http://127.0.0.1:8000/  (publico)
    http://127.0.0.1:8000/admin  (privado)
'''
