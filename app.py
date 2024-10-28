
import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from models import db  # Import db from models.py

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///show.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize db and migrate with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize the API
    api = Api(app)

    # Import and register resources within app context 
    with app.app_context():
        from resources import Episode_List_Resource, Episode_Detail_Resource, Guest_List_Resource, Appearance_Create_Resource
        api.add_resource(Episode_List_Resource, '/episodes')
        api.add_resource(Episode_Detail_Resource, '/episodes/<int:id>')
        api.add_resource(Guest_List_Resource, '/guests')
        api.add_resource(Appearance_Create_Resource, '/appearances')

    with app.app_context():
        db.create_all() 
    return app

if __name__ == '__main__':
    create_app().run(debug=True, port=5555)
