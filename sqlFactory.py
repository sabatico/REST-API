from db import db
from flask_migrate import Migrate

def initialize_DB(app):
    # INIT SQLAlchemy
    db.init_app(app)
    
    #INIT migrate
    initialyze_MIGRATE(app,db)

    return db

def initialyze_MIGRATE(app,db):
    migrate = Migrate(app,db)
    return migrate