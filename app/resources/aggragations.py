from flask_restful import Resource
from sqlalchemy import func

from app import db
from app.database.models import Film


class AggrationAPI(Resource):
    def get(self):
        films_count = db.session.query(func.count(Film.id)).scalar()
        max_rating = db.session.query(func.max(Film.rating)).scalar()
        min_rating = db.session.query(func.min(Film.rating)).scalar()
        avg_rating = db.session.query(func.avg(Film.rating)).scalar()
        sum_rating = db.session.query(func.sum(Film.rating)).scalar()
        
        return {
            'count': films_count,
            'max_rating': max_rating,
            'min_rating': min_rating,
            'average': avg_rating,
            'sum': sum_rating
        }
        