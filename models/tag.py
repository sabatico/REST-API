from factory.dbFactory import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)

    store = db.relationship("StoreModel", back_populates="tags")
    #this tells to cehck in secondary table to get the list of items to wher ethe tags relates to
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")
