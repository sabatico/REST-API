import os as os

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_smorest import Api

from db import db
from models import BlocklistModel
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

# below is like models.__init__ ( we have the 2 import lines in __init__.py inside models, these will be imported automatically here)


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

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # initialises sqlalchemy and connects to our app
    db.init_app(app)

    # this will always run after the app has started, but right before first request ( triggered automatically)
    @app.before_first_request
    def create_tables():
        db.create_all()

    # initiate JWT manager
    app.config["JWT_SECRET_KEY"] = os.environ.get("GWT_SECRET_KEY")
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    # builtindecorator that makes the below function run at tokent use, to check if the token is still good, or already revoked
    def check_if_token_in_bloklist(jwt_header, jwt_payload):
        """the function must take the 2 args from above
        the function will check if the token "jti" value is in BLOCKLIST, and return TRUE if revoked, or false if not"""
        jti = jwt_payload["jti"]

        if BlocklistModel.query.filter(BlocklistModel.jti == jti).first():
            return True
        return False

    @jwt.revoked_token_loader
    # build in decorator for a function that will specify the revoked token message (flask message)
    def revoked_token_callback(jwt_header, jwt_payload):
        return (jsonify({"description": "The token has been revoked", "error": "token_revoked"}), 401)

    @jwt.additional_claims_loader
    # "identity" in function args is coming from identity param that was used  in jwt token creation
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {
            jsonify({"message": "The token has expires.", "error": "token_expired"}),
            401,
        }

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {
            jsonify({"message": "The signature verification failed", "error": "token_invalid"}),
            401,
        }

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {
            jsonify({"description": "Request does not contain an access token", "error": "authorization_required"}),
            401,
        }

    # initiate api
    api = Api(app)

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
