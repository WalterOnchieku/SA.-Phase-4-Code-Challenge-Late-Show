import csv
from app import db, create_app  
from models import Episode, Guest, Appearance 

app = create_app()  # Initialize the Flask app

# Define the path to the CSV file
csv_file_path = 'seed.csv'

def seed_data_from_csv(file_path):
    with app.app_context():  # Ensure the script runs in the app context
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            
            # Store already created episodes and guests to avoid duplicates
            episode_cache = {}
            guest_cache = {}

            for row in reader:
                # Create or get Episode from cache
                episode_date = row['Show']
                if episode_date not in episode_cache:
                    episode = Episode(date=episode_date, number=None)  # number could be None or derived
                    db.session.add(episode)
                    db.session.flush()  # This ensures the episode gets an ID
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

            # Commit all changes to the database
            db.session.commit()
            print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed_data_from_csv('seed.csv')
