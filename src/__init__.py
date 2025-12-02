from flask import Flask
#add later for db
#from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from src.services.db_service import init_database
from src import models
#db = SQLAlchemy()

def create_app():
    load_dotenv()  # Load environment variables from a .env file

    app = Flask(__name__, instance_relative_config=True)

    # load configuration
    #app.config.from_myobject('src.config.Config')
    #app.config.from_pyfile('config.py', silent=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev"),
        #SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL"),
        #SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    #add later for db
    #db.init_app(app)
    init_database(app)

    #with app.app_context():
    #    db.create_all()  # Create database tables for our data models

    # Import and register blueprints here
    #from src.routes.auth_routes import auth_bp
    #app.register_blueprint(auth_bp)

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