from datetime import datetime

from core.configs import DBBaseModel
from models.post_model import PostModel

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class ComentarioModel(DBBaseModel):
    __tablename__: str = 'comentarios'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    data: datetime = Column(DateTime, default=datetime.now, index=True)

    # Chave estrangeira e relacionamento
    from sqlalchemy.orm import Mapped, mapped_column, relationship
    id_post: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id')) # chave estrangeira
    post: Mapped[PostModel] = relationship('PostModel', lazy='joined') # Relacionamento

    autor: str = Column(String(200))
    texto: str = Column(String(400))
