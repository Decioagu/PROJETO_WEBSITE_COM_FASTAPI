from datetime import datetime

from fastapi.routing import APIRouter
from fastapi.requests import Request

from core.configs import settings
from views.admin.membro_admin import membro_admin
from views.admin.area_admin import area_admin
from views.admin.autor_admin import autor_admin
from views.admin.comentario_admin import comentario_admin
from views.admin.duvida_admin import duvida_admin
from views.admin.post_admin import post_admin
from views.admin.projeto_admin import projeto_admin
from views.admin.tag_admin import tag_admin

router = APIRouter(prefix="/admin")
router.include_router(membro_admin.router, prefix="/admin")
router.include_router(area_admin.router, prefix="/admin")
router.include_router(autor_admin.router, prefix="/admin")
router.include_router(comentario_admin.router, prefix="/admin")
router.include_router(duvida_admin.router, prefix="/admin")
router.include_router(post_admin.router, prefix="/admin")
router.include_router(projeto_admin.router, prefix="/admin")
router.include_router(tag_admin.router, prefix="/admin")


@router.get('/', name='admin_index')
async def admin_index(request: Request):
    context = {"request": request, "ano": datetime.now().year}

    return settings.TEMPLATES.TemplateResponse('admin/index.html', context=context)

