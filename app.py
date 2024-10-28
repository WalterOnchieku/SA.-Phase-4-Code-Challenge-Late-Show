from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

# Initialize the db and migrate globally
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    print("Creating Flask app...")
    app = Flask(__name__)

    # Set up the configuration for the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///show.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the db and migrate with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize the Api instance for flask-restful
    api = Api(app)

    # Import routes within the app context to avoid circular imports
    from routes import EpisodeList, EpisodeDetail, GuestList, AppearanceCreate

    # Add resources to the Api instance
    api.add_resource(EpisodeList, '/episodes')             # GET /episodes
    api.add_resource(EpisodeDetail, '/episodes/<int:id>')  # GET /episodes/<id>
    api.add_resource(GuestList, '/guests')                 # GET /guests
    api.add_resource(AppearanceCreate, '/appearances')     # POST /appearances

    return app

if __name__ == '__main__':
    create_app().run(debug=True, port=5555)
