import os
from sqlalchemy import ARRAY, Column, Integer, String, Float, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

Base = declarative_base()


# id,title,synopsis,genre,aired,episodes,members,popularity,ranked,score,img_url,link
class Anime(Base):
    """The Account class corresponds to the "Animes" database table."""

    __tablename__ = "animes"
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String)
    synopsis = Column(String)
    genre = Column(ARRAY(String))
    aired = Column(String)
    episodes = Column(Integer)
    members = Column(Integer)
    popularity = Column(Float)
    ranked = Column(Integer)
    score = Column(Float)
    img_url = Column(String)
    link = Column(String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
