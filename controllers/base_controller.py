from typing import Optional, List

from fastapi.requests import Request
from sqlalchemy.future import select # (consultas assíncronas)

from core.configs import get_session
from models.tag_model import TagModel
from models.autor_model import AutorModel
from models.post_model import PostModel

''''''
class BaseController:

    def __init__(self, request: Request, model: object) -> None:
        self.request: Request = request
        self.model: object = model # tipo genérico de dados


    async def get_all_crud(self) -> Optional[List[object]]:
        """
        Retorna todos os registros do model
        """
        async with get_session() as session:
            query = select(self.model)
            result = await session.execute(query)

            return result.scalars().unique().all()


    async def get_one_crud(self, id_obj: int) -> Optional[object]:
        """
        Retorna o objeto especificado pelo id_obj ou None
        """
        async with get_session() as session:
            obj: self.model = await session.get(self.model, id_obj)

            return obj


    async def post_crud(self) -> None:
        raise NotImplementedError("Você precisa implementar este método.")


    async def put_crud(self, obj: object) -> None:
        raise NotImplementedError("Você precisa implementar este método.")
    
    
    async def del_crud(self, id_obj: int) -> None:
        async with get_session() as session:
            obj: self.model = await session.get(self.model, id_obj)

            if obj:
                await session.delete(obj)
                await session.commit()

    
    # Coleção de métodos comuns usados nas filhas
      
    async def get_tags(self) -> Optional[List[TagModel]]:
        """
        Retorna todos os registros de tag
        """
        async with get_session() as session:
            query = select(TagModel)
            result = await session.execute(query)
            tags: Optional[List[TagModel]] = result.scalars().all()

        return tags
    
    
    async def get_tag(self, id_tag: int) -> TagModel:
        """
        Retorna o objeto especificado pelo id_obj ou None
        """
        async with get_session() as session:
            tag: TagModel = await session.get(TagModel, id_tag)

        return tag


    async def get_autores(self) -> Optional[List[AutorModel]]:
        """
        Retorna todos os registros de autores
        """
        async with get_session() as session:
            query = select(AutorModel)
            result = await session.execute(query)
            autores: Optional[List[AutorModel]] = result.scalars().unique().all()

        return autores
    
    
    async def get_autor(self, id_autor: int) -> AutorModel:
        """
        Retorna o objeto especificado pelo id_obj ou None
        """
        async with get_session() as session:
            autor: AutorModel = await session.get(AutorModel, id_autor)

        return autor

    
    async def get_posts(self) -> Optional[List[PostModel]]:
        """
        Retorna todos os registros de posts
        """
        async with get_session() as session:
            query = select(PostModel)
            result = await session.execute(query)
            autores: Optional[List[PostModel]] = result.scalars().unique().all()

        return autores
    

    async def get_post(self, id_post: int) -> PostModel:
        """
        Retorna o objeto especificado pelo id_obj ou None
        """
        async with get_session() as session:
            post: PostModel = await session.get(PostModel, id_post)

        return post

