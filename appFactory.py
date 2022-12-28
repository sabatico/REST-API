
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

import os as os

# below is like models.__init__ ( we have the 2 import lines in __init__.py inside models, these will be imported automatically here)

from db import db


from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"

    # api documentation app config
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    #initialises sqlalchemy and connects to our app
    db.init_app(app)
    
    #this will always run after the app has started, but right before first request ( triggered automatically)
    @app.before_first_request
    def create_tables():
        db.create_all()
        
        

    
    
    #initiate JWT manager
    app.config["JWT_SECRET_KEY"] = os.environ.get('GWT_SECRET_KEY')
    jwt= JWTManager(app)
    
    # initiate api
    api = Api(app)    

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    
    return app