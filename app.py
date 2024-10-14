from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize the db globally
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Set up the configuration for the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///show.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the db with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Import blueprints and models within the app context
    with app.app_context():
        from models import Episode, Guest, Appearance  # Import  models here to make sure they are registered with SQLAlchemy
        db.create_all()  # Create tables in the database
    
    # Register the blueprint
    # app.register_blueprint(heroes_bp)

    return app
