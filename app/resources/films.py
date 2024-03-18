from flask_restful import Resource
from flask import request
import uuid

from marshmallow import ValidationError

from app import db
from app.database.models import Film
from app.schemas.films import FilmSchema
from app.resources.auth import token_required
from app.services.film_service import FilmService


class FilmListApi(Resource):
    film_schema = FilmSchema()
    
    def get(self, uuid=None):
        if not uuid:
            films = FilmService.fetch_all_films(db.session).all()
            return self.film_schema.dump(films, many=True), 200
        
        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return {'message': 'film not found'}, 404
        
        return self.film_schema.dump(film), 200
    
    # @token_required
    def post(self):
        try:
            film_data = request.json
            film_data['uuid'] = str(uuid.uuid4())
            film = self.film_schema.load(film_data, session=db.session)
        except ValidationError as err:
            return {'message': str(err)}, 400
        db.session.add(film)
        db.session.commit()
        return self.film_schema.dump(film), 201
    
    # @token_required
    def put(self, uuid):
        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return 'not found', 404
        
        try:
            film_data = request.json
            film_data['uuid'] = str(uuid.uuid())
            film = self.film_schema.load(film_data, instance=film, session=db.session)
        except ValidationError as err:
            return {'message': str(err)}, 400
        db.session.add(film)
        db.session.commit()
        return self.film_schema.dump(film), 201
        
    def patch(self, uuid):
        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return 'film not found', 404
        
        try:
            film_json = self.film_schema.load(request.json, partial=True)
        except ValidationError as err:
            return {'message': str(err)}, 400
        
        for attr, value in film_json.items():
            setattr(film, attr, value)
        db.session.commit()
        
        return {'message': 'Updated successfully'}, 200
    
    @token_required
    def delete(self, uuid):
        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return 'film not found', 404
        
        db.session.delete(film)
        db.session.commit()
        