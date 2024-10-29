
import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from models import db  # Import db from models.py

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://my_db_xfw3_user:maZ4f6KPwKFe2ezMzXYhuhJTTQdPlMlh@dpg-csfv6am8ii6s73e62r40-a.oregon-postgres.render.com/my_db_xfw3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.json.compact = False

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

    # with app.app_context():
    #     db.create_all() 
    return app

# if __name__ == '__main__':
#     create_app().run(debug=True, port=5555)
