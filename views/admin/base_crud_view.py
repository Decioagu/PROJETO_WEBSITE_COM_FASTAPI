from fastapi.routing import APIRouter, APIRoute  # Substituição
from fastapi import status
from fastapi.responses import Response
from fastapi.exceptions import HTTPException

from core.configs import settings
from controllers.base_controller import BaseController
from core.deps import valida_login



class BaseCrudView:

    # construtor
    def __init__(self, template_base: str) -> None:
        self.template_base: str = template_base # recebe nome (classe filha)

        self.router = APIRouter()
        self.router.routes.append(APIRoute(path=f"/{self.template_base}/list", endpoint=self.object_list, methods=["GET",], name=f'{self.template_base}_list')) # Substituição
        self.router.routes.append(APIRoute(path=f"/{self.template_base}/create", endpoint=self.object_create, methods=["GET", "POST"], name=f'{self.template_base}_create')) # Substituição
        self.router.routes.append(APIRoute(path=f"/{self.template_base}/details/"+'{obj_id:int}', endpoint=self.object_edit, methods=["GET",], name=f'{self.template_base}_details')) # Substituição
        self.router.routes.append(APIRoute(path=f"/{self.template_base}/edit/"+'{obj_id:int}', endpoint=self.object_edit, methods=["GET", "POST"], name=f'{self.template_base}_edit')) # Substituição
        self.router.routes.append(APIRoute(path=f"/{self.template_base}/delete/"+'{obj_id:int}', endpoint=self.object_delete, methods=["DELETE",], name=f'{self.template_base}_delete')) # Substituição


    async def object_create(self) -> Response:
        """
        Rota para carregar o template do formulário e criar um objeto [GET, POST]
        """
        raise NotImplementedError("Você precisa implementar este método.")


    async def object_edit(self) -> Response:
        """
        Rota para carregar o template do formulário de edição e atualizar um objeto [GET, POST]
        """
        raise NotImplementedError("Você precisa implementar este método.")
     
    ### Validação do login
    async def object_list(self, object_controller: BaseController) -> Response:
        """
        Rota para listar todos os objetos [GET]
        """
        # Validação do login do membro através do cookie de autenticação ("auth_cookie")
        context = await valida_login(object_controller.request)

        # Se o membro não estiver autenticado ("auth_cookie")
        try:
           if not context["membro"]:
               return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)

        dados = await object_controller.get_all_crud()

        context.update({"dados": dados}) # adiciona os dados ao contexto

        return settings.TEMPLATES.TemplateResponse(f"admin/{self.template_base}/list.html", context=context)

    ### Validação do login
    async def object_delete(self, object_controller: BaseController, obj_id: int) -> Response:
        """
        Rota para deletar um objeto [DELETE]
        """
        # Validação do login do membro através do cookie de autenticação ("auth_cookie")
        context = await valida_login(object_controller.request)

        # Se o membro não estiver autenticado ("auth_cookie")
        try:
           if not context["membro"]:
               return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)

        objeto = await object_controller.get_one_crud(id_obj=obj_id)

        # Se o objeto não existir
        if not objeto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        # Se o objeto for o primeiro (id=1), não pode ser deletado
        if obj_id == 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não pode deletar este objeto.")
        
        # Deletar o objeto
        await object_controller.del_crud(id_obj=objeto.id)

        return  Response(str(object_controller.request.url_for(f"{self.template_base}_list")))

    ### Validação do login
    async def object_details(self, object_controller: BaseController, obj_id: int) -> Response:
        """
        Rota para apresentar os detalhes de um objeto [GET]
        """
        # Validação do login do membro através do cookie de autenticação ("auth_cookie")
        context = await valida_login(object_controller.request)

        # Se o membro não estiver autenticado ("auth_cookie")
        try:
           if not context["membro"]:
               return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)

        # Adicionar o request no context
        objeto = await object_controller.get_one_crud(id_obj=obj_id)

        if not objeto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        context.update({"objeto": objeto})

        if 'details' in str(object_controller.request.url):
            return settings.TEMPLATES.TemplateResponse(f"admin/{self.template_base}/details.html", context=context)
        
        elif 'edit' in str(object_controller.request.url):
            return settings.TEMPLATES.TemplateResponse(f"admin/{self.template_base}/edit.html", context=context)
        
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

