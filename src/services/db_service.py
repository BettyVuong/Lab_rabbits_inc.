#good websites
# https://flask-migrate.readthedocs.io/en/latest/
# https://python-adv-web-apps.readthedocs.io/en/latest/flask_db1.html
# https://python-adv-web-apps.readthedocs.io/en/latest/index.html

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_database(app):
    db.init_app(app)
    migrate.init_app(app, db)


