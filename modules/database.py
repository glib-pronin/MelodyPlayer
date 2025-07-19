from sqlalchemy import Column, String, Integer, create_engine, select, func
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

    def __repr__(self):
        return f"title - {self.title}, artist - {self.artist}"

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

# Повернення списку
def get_playlist(artist="", track=""):
    artist_stmt = f"%{artist.lower()}%"
    track_stmt = f"%{track.lower()}%"
    with Session() as session:
        playlist = session.execute(select(Track).where(
            func.lower(Track.title).like(track_stmt) & func.lower(Track.artist).like(artist_stmt)
            )).scalars().all()
    return form_response(playlist)

# Перетворення списку об'єктів в словник потрібної формації
def form_response(playlist):
    playlist_dict = {"current_track": 0, "tracks": {}}
    for ind, track in enumerate(playlist):
        playlist_dict["tracks"][ind+1] = track
    return playlist_dict

def add_track_to_db(title, artist, filename, duration):
    with Session() as session:
        track = Track(title=title, artist=artist, filepath=f"assets/music/{filename}", duration=duration)
        session.add(track)
        session.commit()
        