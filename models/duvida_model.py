from core.configs import DBBaseModel
from models.area_model import AreaModel

from sqlalchemy import Column, Integer, String, ForeignKey

class DuvidaModel(DBBaseModel):
    __tablename__: str = 'duvida'

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    # Chave estrangeira e relacionamento
    from sqlalchemy.orm import Mapped, mapped_column, relationship
    id_area: Mapped[int] = mapped_column(Integer, ForeignKey('areas.id')) # chave estrangeira
    area: Mapped[AreaModel] = relationship('AreaModel', lazy='joined') # Relacionamento

    titulo: str = Column(String(200))
    resposta: str = Column(String(400))

    

