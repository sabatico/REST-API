import os as os

from flask import Flask

import apiFactory as apiFactory
import jwtFactory as jwtFactory
import sqlFactory as sqlFactory


# below is like models.__init__ ( we have the 2 import lines in __init__.py inside models, these will be imported automatically here)


def create_app(db_url=None):
    # INIT APP
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"

    # API configs
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # JWT configs
    app.config["JWT_SECRET_KEY"] = os.environ.get("GWT_SECRET_KEY")

    # INIT  sqlalchemy and migrate
    sqlFactory.initialize_DB(app)
    
    
    # INIT JWT manager
    jwtFactory.initialyze_JWT(app)
    # INIT API
    apiFactory.initialyze_API(app)
    

    return app
