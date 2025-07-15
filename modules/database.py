from sqlalchemy import Column, String, Integer, create_engine, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine(url='sqlite:///melody_player.db')

class Base(DeclarativeBase):
    pass

class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    artist = Column(String)
    filepath = Column(String, unique=True)
    duration = Column(Integer)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

def get_playlist():
    with Session() as session:
        playlist = session.execute(select(Track)).scalars().all()
        return playlist

get_playlist()