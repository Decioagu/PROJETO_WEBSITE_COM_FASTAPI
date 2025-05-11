from core.configs import DBBaseModel

from sqlalchemy import Column, Integer, String


class TagModel(DBBaseModel):
    """Temos tags em várias partes do website"""
    __tablename__: str = 'tags'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    tag: str = Column(String(100))

