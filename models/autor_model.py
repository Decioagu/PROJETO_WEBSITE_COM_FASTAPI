from typing import List

from sqlalchemy import Table, Column, Integer, String, ForeignKey

from core.configs import DBBaseModel
from models.tag_model import TagModel


# Autor pode ter várias tags | relacionamento (muitos-para-muitos)
tags_autor = Table(
    'tags_autor', # nome
    DBBaseModel.metadata, # manipula estrutura do banco de dados com tabelas associadas (contêiner)
    Column('id_autor', Integer, ForeignKey('autores.id')),
    Column('id_tag', Integer, ForeignKey('tags.id'))
)


class AutorModel(DBBaseModel):
    """Autor das postagens no blog"""
    __tablename__: str = 'autores'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100))
    imagem: str = Column(String(100)) # 40x40

    # Chave estrangeira e relacionamento
    from sqlalchemy.orm import Mapped, mapped_column, relationship
    # tags = tabela secundaria "tags_autor"
    tags: Mapped[List[TagModel]] = relationship('TagModel', secondary=tags_autor, backref='taga', lazy='joined') # Relacionamento
    
    @property
    def get_tags_list(self):
        lista: List[int] = []

        for tag in self.tags:
            lista.append(int(tag.id))
        
        return lista
