from fastapi.routing import APIRouter
from fastapi.requests import Request

## instância de conexão Banco de Dados
from core.configs import settings

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