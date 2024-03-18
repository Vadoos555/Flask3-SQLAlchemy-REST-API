import uuid

from app import db

from sqlalchemy import Integer, String, Float, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from werkzeug.security import generate_password_hash


movies_actors = db.Table(
    'movies_actors',
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True),
    db.Column('film_id', db.Integer, db.ForeignKey('films.id'), primary_key=True)
)


class Film(db.Model):
    __tablename__ = 'films'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    release_date: Mapped[Date] = mapped_column(Date, nullable=False)
    uuid: Mapped[str] = mapped_column(String(36), unique=True)
    description: Mapped[str] = mapped_column(db.Text)
    distributed_by: Mapped[str] = mapped_column(String(128), nullable=False)
    length: Mapped[float] = mapped_column(Float)
    rating: Mapped[float] = mapped_column(Float)
    actors = relationship('Actor', secondary=movies_actors, lazy='subquery', backref=backref('films', lazy=True))
    
    def __init__(self, title, release_date, description, distributed_by, length, rating, actors=None, uuid=None):
        self.title = title
        self.release_date = release_date
        self.uuid = uuid or str(uuid.uuid4())
        self.description = description
        self.distributed_by = distributed_by
        self.length = length
        self.rating = rating
        if not actors:
            self.actors = []
        else:
            self.actors = actors
    
    def __repr__(self) -> str:
        return f'Film({self.title}, {self.release_date}, {self.uuid}, {self.distributed_by}, {self.rating}, {self.actors})'
    

class Actor(db.Model):
    __tablename__ = 'actors'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    birthday: Mapped[Date] = mapped_column(Date)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    
    def _repr__(self):
        return f'Actor({self.name}, {self.birthday})'
    
    
class User(db.Model):
    __tablename__ = 'users'
    
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(50), unique=True, nullable=False)
    email = mapped_column(String(50), unique=True, nullable=False)
    password = mapped_column(String(254), nullable=False)
    is_admin = mapped_column(Boolean, default=False)
    uuid = mapped_column(String(36), unique=True)
    
    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin
        self.uuid = str(uuid.uuid4())
    
    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.uuid})'
    
    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_user_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()
    