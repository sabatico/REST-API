from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def initialize_DB(app):
    # INIT SQLAlchemy
    db.init_app(app)

    # INIT migrate
    initialyze_MIGRATE(app, db)

    return db


def initialyze_MIGRATE(app, db):
    migrate = Migrate(app, db, render_as_batch=True)
    return migrate
