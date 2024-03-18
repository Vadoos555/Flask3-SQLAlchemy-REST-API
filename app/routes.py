from app import api

from app.resources.films import FilmListApi
from app.resources.actors import ActorListApi
from app.resources.smoke import Smoke
from app.resources.aggragations import AggrationAPI
from app.resources.auth import AuthRegister, AuthLogin
from app.resources.populate_db import PopulateDB, PopulateDBThreaded, PopulateDBThreadPoolExecutor


api.add_resource(Smoke, '/smoke', strict_slashes=False)
api.add_resource(FilmListApi, '/films', '/films/<uuid>', strict_slashes=False)
api.add_resource(ActorListApi, '/actors', '/actors/<id>', strict_slashes=False)
api.add_resource(AggrationAPI, '/aggragations', strict_slashes=False)
api.add_resource(AuthRegister, '/register', strict_slashes=False)
api.add_resource(AuthLogin, '/login', strict_slashes=False)
api.add_resource(PopulateDB, '/populate_db', strict_slashes=False)
api.add_resource(PopulateDBThreaded, '/populate_db_thread', strict_slashes=False)
api.add_resource(PopulateDBThreadPoolExecutor, '/populate_db_executor', strict_slashes=False)
