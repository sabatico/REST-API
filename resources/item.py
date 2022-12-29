from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError


from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operation on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, validated_item_data, item_id):
        '''PUT expects to UPDATE if already exists
        or CREATE if item is not existent'''
        
        #use get() withotu 404 check
        item = ItemModel.query.get(item_id)
        
        #if item exists - update, else - create
        if item:
            item.price = validated_item_data["price"]
            item.name = validated_item_data["name"]
                        
        else:
            #the 'id' of the item will be taken from put query
            item = ItemModel(id=item_id,**validated_item_data)
        
        db.session.add(item)
        db.session.commit()
        
        return item
    
    @jwt_required()
    def delete(self, item_id):
        #below check the is_admin token CLAM , if its True -> permit deleting, else -> abort
        jwt = get_jwt()
        if not jwt.get('is_admin'):
            abort(401,message="Admin privilege required")
            
        item = ItemModel.query.get_or_404(item_id)
        
        db.session.delete(item)
        db.session.commit()
        
        
        return {"message": "Item deleted successfully"}

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, validated_item_data):
        """ creates an item in a store"""
        item = ItemModel(**validated_item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item")

        return item
    
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        """ gets all items from all stores"""
        item = ItemModel.query.all()
        return item
