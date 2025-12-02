####

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

#good websites
# https://flask-migrate.readthedocs.io/en/latest/
# https://python-adv-web-apps.readthedocs.io/en/latest/flask_db1.html
# https://python-adv-web-apps.readthedocs.io/en/latest/index.html

db = SQLAlchemy()

migrate = Migrate()

def init_database(app):

    #get url from .env file
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

    db.init_app(app)
    migrate.init_app(app, db)

