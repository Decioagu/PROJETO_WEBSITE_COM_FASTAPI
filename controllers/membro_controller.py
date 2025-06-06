from fastapi.requests import Request
from fastapi import UploadFile
from typing import Optional
from sqlalchemy.future import select

from aiofile import async_open # Upload do arquivo
from uuid import uuid4 # Gera um nome aleatório

from core.configs import get_session, settings
from models.membro_model import MembroModel
from controllers.base_controller import BaseController
from core.auth import gerar_hash_senha, verificar_hash_senha


class MembroController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, MembroModel)
    
    async def post_crud(self) -> None:
        # Recebe dados do form
        form = await self.request.form()
        
        nome: str = form.get('nome')
        funcao: str = form.get('funcao')
        imagem: UploadFile = form.get('imagem')
        email: str = form.get('email') 
        senha: str = form.get('senha')
        hash_senha: str = gerar_hash_senha(senha=senha) # Gera o hash da senha

        # Nome aleatório para a imagem
        arquivo_ext: str = imagem.filename.split('.')[-1]
        novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"

        # Instanciar o objeto
        membro: MembroModel = MembroModel(nome=nome, funcao=funcao, imagem=novo_nome, email=email, senha=hash_senha) ###

        # Fazer o upload do arquivo
        async with async_open(f"{settings.MEDIA}/membro/{novo_nome}", "wb") as afile:
            await afile.write(imagem.file.read())
        
        # Cria a sessão e insere no banco de dados
        async with get_session() as session:
            session.add(membro)
            await session.commit()
 

    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            membro: MembroModel = await session.get(self.model, obj.id)

            if membro:
                # Recebe os dados do form
                form = await self.request.form()

                nome: str = form.get('nome')
                funcao: str = form.get('funcao')
                imagem: UploadFile = form.get('imagem')
                email: str = form.get('email') 
                senha: str = form.get('senha')
                hash_senha: str = gerar_hash_senha(senha=senha) # Gera o hash da senha

                if nome and nome != membro.nome:
                    membro.nome = nome
                if funcao and funcao != membro.funcao:
                    membro.funcao = funcao
                if email and email != membro.email:
                    membro.email = email
                if senha  and hash_senha != membro.senha: # Verifica se a senha foi alterada
                    membro.senha = hash_senha
                if imagem.filename:
                    # Gera um nome aleatório
                    arquivo_ext: str = imagem.filename.split('.')[-1]
                    novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"
                    membro.imagem = novo_nome
                    # Faz o upload da imagem
                    async with async_open(f"{settings.MEDIA}/membro/{novo_nome}", "wb") as afile:
                        await afile.write(imagem.file.read())
                await session.commit()

# ================================ LOGIN =================================

    async def login_membro(self, email: str, senha: str) -> Optional[MembroModel]:
        """
        Validar o login do membro através do email e senha no Banco de Dados.
        """
        async with get_session() as session:
            query = select(MembroModel).filter(MembroModel.email == email)
            results = await session.execute(query)

            membro = results.scalar_one_or_none()

            if not membro:
                return None
            # Verifica se a senha informada é igual ao hash da senha do membro
            if not verificar_hash_senha(senha=senha, hash_senha=membro.senha):
                return None
            
            return membro

