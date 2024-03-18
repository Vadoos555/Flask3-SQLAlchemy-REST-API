from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from flask_swagger_ui import get_swaggerui_blueprint

import config


class Base(DeclarativeBase):
  pass


app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(model_class=Base)
db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
  SWAGGER_URL,
  API_URL,
  config={'app_name': 'Flask_rest_api'}
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

from app import routes
from .database import models
