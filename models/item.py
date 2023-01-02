from factory.dbFactory import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)

    # this below helps using item.store to getthe associated StoresModel item  (associated to the foreign key id)
    # back_populates='items'  -> this permits the STORE item also acces the item item ( check the config of the store now, it has item)
    store = db.relationship("StoreModel", back_populates="items")
    # back populates items and looks inside item_tags for the list of tags
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
