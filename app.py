import os
import csv
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from models import db, Episode, Guest, Appearance  # Import db and models

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize db and migrate with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize the API
    api = Api(app)

    # Import and register resources within app context 
    with app.app_context():
        from resources import (
            Episode_List_Resource,
            Episode_Detail_Resource,
            Guest_List_Resource,
            Appearance_Create_Resource
        )
        api.add_resource(Episode_List_Resource, '/episodes')
        api.add_resource(Episode_Detail_Resource, '/episodes/<int:id>')
        api.add_resource(Guest_List_Resource, '/guests')
        api.add_resource(Appearance_Create_Resource, '/appearances')

        # Run seeding if environment variable is set
        db.create_all()
        if os.getenv("SEED_DB") == "True":
            seed_data_from_csv('seed.csv')

    return app

def seed_data_from_csv(file_path):
    """Seeds the database from a CSV file if it is currently empty."""
    if db.session.query(Episode).count() > 0:
        print("Database already seeded!")
        return

    print("Seeding database...")
    episode_cache = {}
    guest_cache = {}

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Create or get Episode from cache
            episode_date = row['Show']
            if episode_date not in episode_cache:
                episode = Episode(date=episode_date, number=None)
                db.session.add(episode)
                db.session.flush()  # Ensure episode gets an ID
                episode_cache[episode_date] = episode
            else:
                episode = episode_cache[episode_date]

            # Create or get Guest from cache
            guest_name = row['Raw_Guest_List']
            occupation = row['GoogleKnowlege_Occupation']
            if guest_name not in guest_cache:
                guest = Guest(name=guest_name, occupation=occupation)
                db.session.add(guest)
                db.session.flush()  # Ensure guest gets an ID
                guest_cache[guest_name] = guest
            else:
                guest = guest_cache[guest_name]

            # Create Appearance linking Guest and Episode
            appearance = Appearance(episode_id=episode.id, guest_id=guest.id, rating=None)
            db.session.add(appearance)

    db.session.commit()
    print("Database seeding completed successfully!")

# Uncomment for local testing
# if __name__ == '__main__':
#     create_app().run(debug=True, port=5555)
