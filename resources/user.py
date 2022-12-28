from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint("users", __name__, description="Operation on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201,UserSchema)
    def post(self,validated_user_data):
        print(validated_user_data)
        user = UserModel(
            username = validated_user_data["username"],
            password = pbkdf2_sha256.hash(validated_user_data["password"])
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            
        #uniqueness validation exception
        except IntegrityError:
            abort(400,message="User already exists")
        #any other errors    
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item")

        return {"message": "User added successfully"},201

@blp.route("/users")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        users =UserModel.query.all()
        return users

    
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
      
        db.session.delete(user)
        db.session.commit()
         
        return {"message": "User deleted successfully"},200