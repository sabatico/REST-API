from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from sqlFactory import db
from models import ItemModel, StoreModel, TagModel
from schemas import TagAndItemSchema, TagSchema

blp = Blueprint("tags", __name__, description="Operation on tags")


@blp.route("/store/<int:store_id>/tag")
class TagList(MethodView):
    
    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, validated_tag_data, store_id):
        # wewill craete tag item, and add it a store_id from the post query itself
        tag = TagModel(**validated_tag_data, store_id=store_id)

        # check if tag with this name exists in the store related to store_id
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == validated_tag_data["name"]).first():
            abort("message", "This tag already exits in targeted store")

        # try puting in db
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag

    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        # because of modelinheritance, we can:
        # 1. Get the sotre by store_id
        store = StoreModel.query.get_or_404(store_id)
        # use store.tags to get the list of items
        # this is still query, so we use .all()
        return store.tags.all()


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LingTagsToItem(MethodView):
    """Add or Removes a row in 'items_tags' AND in 'items' tables"""
    
    @jwt_required()
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        # retireve item with item_id from Items table
        item = ItemModel.query.get_or_404(item_id)
        # retirieve tag with tag_id from tags table
        tag = TagModel.query.get_or_404(tag_id)

        # we can append data because the target table (item.tags) is a list
        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag

    @jwt_required()
    @blp.response(201, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        # retireve item with item_id from Items table
        item = ItemModel.query.get_or_404(item_id)
        # retirieve tag with tag_id from tags table
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return {"message": "Item deleted successfully", "item": item, "tag": tag}


@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    
    @jwt_required()
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return tag

    @jwt_required()
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return {"message": "Item removed from tag", "item": item, "tag": tag}



@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(201, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @jwt_required()
    @blp.response(202, description="Deletes tag if no item is tagged with it")
    @blp.alt_response(404, description="Tag not found")
    @blp.alt_response(400, description="Returned when the tag is assigned to an item a nd can not be deleted")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any items, then try again.",
        )
