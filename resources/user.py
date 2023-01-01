from flask.views import MethodView
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, create_refresh_token, get_jwt_identity
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import BlocklistModel, UserModel
from schemas import UserSchema

blp = Blueprint("users", __name__, description="Operation on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, validated_user_data):
        user = UserModel(
            username=validated_user_data["username"], password=pbkdf2_sha256.hash(validated_user_data["password"])
        )

        try:
            db.session.add(user)
            db.session.commit()

        # uniqueness validation exception
        except IntegrityError:
            abort(400, message="User already exists")
        # any other errors
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item")

        return {"message": "User added successfully"}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, validated_user_data):
        user = UserModel.query.filter(UserModel.username == validated_user_data["username"]).first()

        if user and pbkdf2_sha256.verify(validated_user_data["password"], user.password):
            # creates an access token that contains USER ID for further identification
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}

        return {"message": "bad password or nonexisting user"}, 500


@blp.route("/refresh")
class UserTokenRefresh(MethodView):
    #specify that only refresh_token is needed for next steps
    @jwt_required(refresh=True)
    
    def post(self):
        #get user identity from token
        current_user = get_jwt_identity()
        #create new access token with NON-fresh status
        new_token = create_access_token(identity=current_user, fresh=False)
        
        #To only permit token refresh to be done 1 time, we need to add token JTI in blocklist now, as example
        
      
        

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        # "get_gwt()['jti'] -> this extracts the token ID from the whole token"
        token = BlocklistModel(jti=get_jwt()["jti"])
        
        
        try:
            db.session.add(token)
            db.session.commit()

        # uniqueness validation exception
        except IntegrityError:
            abort(400, message="Token already exists")
        # any other errors
        except SQLAlchemyError:
            abort(500, message="An error occurred while revoking the token")

        return {"message": "token revoked and logged out"}, 201


@blp.route("/users")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()

        return {"message": "User deleted successfully"}, 200
