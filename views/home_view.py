from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi import status
from fastapi.exceptions import HTTPException

## instância de conexão Banco de Dados
from core.configs import settings
from core.auth import set_auth, unset_auth
# from core.auth import set_auth, unset_auth
from controllers.membro_controller import MembroController

router = APIRouter() ## roteador de rotas

# Declaração de rotas do arquivo templates/base.html
@router.get('/', name='index')
async def index(request: Request):
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('home/index.html', context=context)
    ## settings.TEMPLATES: Acesso pasta templates 

@router.get('/about', name='about')
async def about(request: Request):
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('home/about.html', context=context)
    ## settings.TEMPLATES: Acesso pasta templates 

@router.get('/contact', name='contact')
async def contact(request: Request):
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('home/contact.html', context=context)
    ## settings.TEMPLATES: Acesso pasta templates 

@router.get('/pricing', name='pricing')
async def pricing(request: Request):
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('home/pricing.html', context=context)
    ## settings.TEMPLATES: Acesso pasta templates 

@router.get('/faq', name='faq')
async def faq(request: Request):
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('home/faq.html', context=context)
    ## settings.TEMPLATES: Acesso pasta templates 

@router.get('/blog', name='blog')
async def blog(request: Request):
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('home/blog.html', context=context)
    ## settings.TEMPLATES: Acesso pasta templates 

@router.get('/blog_post', name='blog_post')
async def blog_post(request: Request, slug: str = ''):
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('home/blog_post.html', context=context)
    ## settings.TEMPLATES: Acesso pasta templates 

@router.get('/portfolio', name='portfolio')
async def portfolio(request: Request):
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('home/portfolio.html', context=context)
    ## settings.TEMPLATES: Acesso pasta templates 

@router.get('/portfolio_item', name='portfolio_item')
async def portfolio_item(request: Request):
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('home/portfolio_item.html', context=context)
    ## settings.TEMPLATES: Acesso pasta templates 

# ==================================== LOGIN =========================================

# Pagina de entrada do login 
@router.get('/login', name='get_login')
async def get_login(request: Request) -> Response:
    context = {
        "request": request
    }
    return settings.TEMPLATES.TemplateResponse('login.html', context=context)


# Acesso ao login do usuário
@router.post('/login', name='post_login')
async def post_login(request: Request) -> Response:
    
    # Instância do controller de membro
    membro_controller: MembroController = MembroController(request)

    # Receber dados do form (HTML)
    form = await request.form()
    email: str = form.get('email')
    senha: str = form.get('senha')

    # Verifica se o email e senha estão preenchidos
    membro = await membro_controller.login_membro(email=email, senha=senha)

    # Se o membro não for encontrado ou a senha estiver incorreta
    if not membro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # redirecionar para URL
    response = RedirectResponse(request.url_for('admin_index'), status_code=status.HTTP_302_FOUND) 

    # Adiciona o cookie na response (auto autenticação do usuário logado)
    set_auth(response=response, membro_id=membro.id)

    return response


# Sair do login usuário
@router.get('/logout', name='logout')
async def logout(request: Request) -> Response:
    # redirecionar para URL
    response = RedirectResponse(request.url_for('index'), status_code=status.HTTP_302_FOUND)

    # Finaliza o cookie na response (auto autenticação do usuário logado)
    unset_auth(response=response)

    return response