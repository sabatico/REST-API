import uuid as uuid

from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

import schemas as schemas

from schemas import StoreSchema, StoreUpdateSchema

blp = Blueprint("stores", __name__, description="Operation on stores")


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.arguments(StoreUpdateSchema)
    @blp.response(201, StoreSchema)
    def put(self, validated_store_data, store_id):
        '''PUT expects to UPDATE if already exists
        or CREATE if item is not existent'''
        
        #use get() withotu 404 check
        store = StoreModel.query.get(store_id)
        
        #if item exists - update, else - create
        if store:
            store.name = validated_store_data["name"]
                        
        else:
            #the 'id' of the item will be taken from put query
            store = StoreModel(id=store_id,**validated_store_data)
        
        db.session.add(store)
        db.session.commit()
        
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
      
        db.session.delete(store)
        db.session.commit()
         
        return {"message": "Store deleted successfully"}

    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store


@blp.route("/store")
class StoreList(MethodView):
    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self, validated_store_data):
        store = StoreModel(**validated_store_data)
        try:
            db.session.add(store)
            db.session.commit()
            
        #uniqueness validation exception
        except IntegrityError:
            abort(400,message="Store already exists")
        #any other errors    
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item")

        return store


    @blp.response(200, StoreSchema(many=True))
    def get(self):
        stores =StoreModel.query.all()
        return stores