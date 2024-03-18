from flask_restful import Resource
from flask import request

from marshmallow import ValidationError

from app import db
from app.database.models import  Actor
from app.schemas.actors import  ActorSchema
from app.resources.auth import token_required
from app.services.actor_service import ActorService


class ActorListApi(Resource):
    actor_schema = ActorSchema()
    
    def get(self, id=None):
        if not id:
            actors = ActorService.fetch_all_actors(db.session).all()
            return self.actor_schema.dump(actors, many=True), 200
        
        actor = db.session.query(Actor).filter_by(id=int(id)).first()
        if not actor:
            return {'message': 'actor not found'}, 404
        
        return self.actor_schema.dump(actor), 200
    
    # @token_required
    def post(self):
        try:
            actor = self.actor_schema.load(request.json, session=db.session)
        except ValidationError as err:
            return {'message': str(err)}, 400
        db.session.add(actor)
        db.session.commit()
        return self.actor_schema.dump(actor), 201
    
    def put(self, id):
        actor = ActorService.fetch_actor_by_id(db.session, id)
        if not actor:
            return 'not found', 404
        
        try:
            actor = self.actor_schema.load(request.json, instance=actor, session=db.session)
        except ValidationError as err:
            return {'message': str(err)}, 400
        db.session.add(actor)
        db.session.commit()
        return self.actor_schema.dump(actor), 201
        
    def patch(self, id):
        actor = ActorService.fetch_actor_by_id(db.session, id)
        if not actor:
            return ' not found', 404
        
        try:
            actor_json = self.actor_schema.load(request.json, partial=True)
        except ValidationError as err:
            return {'message': str(err)}, 400
        
        for attr, value in actor_json.items():
            setattr(actor, attr, value)
        db.session.commit()
        
        return {'message': 'Updated successfully'}, 200
    
    @token_required
    def delete(self, id):
        actor = ActorService.fetch_actor_by_id(db.session, id)
        if not actor:
            return ' not found', 404
        
        db.session.delete(actor)
        db.session.commit()
        