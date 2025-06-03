from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi import status

from core.configs import settings
from views.admin.membro_admin import membro_admin
from views.admin.area_admin import area_admin
from views.admin.autor_admin import autor_admin
from views.admin.comentario_admin import comentario_admin
from views.admin.duvida_admin import duvida_admin
from views.admin.post_admin import post_admin
from views.admin.projeto_admin import projeto_admin
from views.admin.tag_admin import tag_admin
from core.deps import valida_login #

'''
Eliminação de "prefix="/admin" devido:
Substituição de Route por APIRoute em "base_crud_views.py"
'''

router = APIRouter(prefix="/admin")
router.include_router(membro_admin.router) # eliminar "prefix="/admin"
router.include_router(area_admin.router) # eliminar "prefix="/admin" 
router.include_router(autor_admin.router) # eliminar "prefix="/admin"
router.include_router(comentario_admin.router) # eliminar "prefix="/admin"
router.include_router(duvida_admin.router) # eliminar "prefix="/admin"
router.include_router(post_admin.router) # eliminar "prefix="/admin" 
router.include_router(projeto_admin.router) # eliminar "prefix="/admin"
router.include_router(tag_admin.router) # eliminar "prefix="/admin" 

### Validação do login
@router.get('/', name='admin_index')
async def admin_index(request: Request):
    # Validação do login do membro através do cookie de autenticação ("auth_cookie")
    context = await valida_login(request)

    # Se o membro não estiver autenticado ("auth_cookie")
    try:
        if not context["membro"]:
            return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
    
    # redirecionar para URL index
    return settings.TEMPLATES.TemplateResponse('admin/index.html', context=context)