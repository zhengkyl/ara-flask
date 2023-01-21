from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Anime(Base):
    """The Account class corresponds to the "Animes" database table.
    """
    __tablename__ = 'animes'
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String)
    synopsis = Column(String)
    score = Column(Float)
