from factory.dbFactory import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True,nullable=False)
    
    #used to access all assigned items of this store
    #back_populates="store" -> here shows the field in ItemModel where it conneccts
    #lazy="dynamic"  -> items in items will not be fetchet untill asked ( no prefetch)
    #cascade="all, delete, delete-orphan" -> makes it subsequently delete all nested items from ITEMS table
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic",  cascade="all, delete")
    #tags relationship
    tags= db.relationship("TagModel", back_populates="store", lazy="dynamic")