from flask import jsonify
from flask_jwt_extended import JWTManager

from models import BlocklistModel


def initialyze_JWT(app):
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

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (jsonify({"description": "The token is not fresh", "error": "Fresh_token_required"}), 401)

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

    return jwt
