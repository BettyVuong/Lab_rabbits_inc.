from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from src.services.db_service import init_database
from src import models

def create_app():
    load_dotenv()  # Load environment variables from a .env file

    app = Flask(__name__)


    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set")

    # load configuration
    #app.config.from_myobject('src.config.Config')
    #app.config.from_pyfile('config.py', silent=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    init_database(app)

    # Register blueprints
    from src.routes.auth_routes import auth_bp
    from src.routes.main_routes import main_bp
    from src.routes.dashboard_routes import dashboard_bp
    from src.routes.quiz_routes import quiz_bp
    from src.routes.review_routes import review_bp
    #from src.routes.teacher_routes import create_quiz_bp
    from src.routes.teacher_routes import teacher_bp
    from src.routes.teacher_dashboard_routes import teacher_dashboard_bp
    from src.routes.profile_route import profile_bp
    #from src.routes.quiz_routes import quiz_submit_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(review_bp)
    #app.register_blueprint(create_quiz_bp)

    app.register_blueprint(teacher_bp)
    app.register_blueprint(teacher_dashboard_bp)
    app.register_blueprint(profile_bp)

    return app