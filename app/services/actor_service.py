from app import db
from app.database.models import Actor

class ActorService:
    @staticmethod
    def fetch_all_actors(session):
        return session.query(Actor)
    
    @classmethod
    def fetch_actor_by_id(cls, session, actor_id):
        return cls.fetch_all_actors(session).filter_by(id=actor_id).first()
