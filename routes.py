from flask import jsonify, request
from flask_restful import Api, Resource
from models import Episode, Guest, Appearance
from app import db  # Importing db to use for database operations

# Initialize the Api instance (usually done in app.py)
api = Api()

# =====================================================================
# Resource: EpisodeList (Handles GET /episodes)
# =====================================================================
class EpisodeList(Resource):
    # GET request to retrieve a list of all episodes
    def get(self):
        episodes = Episode.query.all()  # Query all Episode records from the database
        
        # Convert each episode to a dictionary for JSON serialization
        episode_list = [
            {
                "id": episode.id,
                "date": episode.date,
                "number": episode.number
            }
            for episode in episodes
        ]
        return episode_list, 200  # Return the list with a 200 (OK) status

# =====================================================================
# Resource: EpisodeDetail (Handles GET /episodes/<id>)
# =====================================================================
class EpisodeDetail(Resource):
    # GET request to retrieve details of a specific episode by ID
    def get(self, id):
        episode = Episode.query.get(id)  # Query the database for an episode by ID
        if not episode:
            return {"error": "Episode not found"}, 404  # Return 404 if episode doesn't exist

        # Prepare episode details with appearances
        episode_data = {
            "id": episode.id,
            "date": episode.date,
            "number": episode.number,
            "appearances": []
        }

        # Query appearances associated with this episode and add to response
        appearances = Appearance.query.filter_by(episode_id=episode.id).all()
        for appearance in appearances:
            appearance_data = {
                "id": appearance.id,
                "episode_id": appearance.episode_id,
                "guest_id": appearance.guest_id,
                "rating": appearance.rating,
                "guest": {
                    "id": appearance.guest.id,
                    "name": appearance.guest.name,
                    "occupation": appearance.guest.occupation
                }
            }
            episode_data["appearances"].append(appearance_data)

        return episode_data, 200  # Return the episode data with a 200 (OK) status

# =====================================================================
# Resource: GuestList (Handles GET /guests)
# =====================================================================
class GuestList(Resource):
    # GET request to retrieve a list of all guests
    def get(self):
        guests = Guest.query.all()  # Query all Guest records from the database
        
        # Convert each guest to a dictionary for JSON serialization
        guest_list = [
            {
                "id": guest.id,
                "name": guest.name,
                "occupation": guest.occupation
            }
            for guest in guests
        ]
        return guest_list, 200  # Return the list with a 200 (OK) status

# =====================================================================
# Resource: AppearanceCreate (Handles POST /appearances)
# =====================================================================
class AppearanceCreate(Resource):
    # POST request to create a new appearance record
    def post(self):
        data = request.get_json()  # Get JSON data from the request body
        rating = data.get('rating')
        episode_id = data.get('episode_id')
        guest_id = data.get('guest_id')

        # Validate rating to ensure it is between 1 and 5
        if not (1 <= rating <= 5):
            return {"errors": ["Rating must be between 1 and 5"]}, 400

        # Check if the referenced episode exists
        episode = Episode.query.get(episode_id)
        if not episode:
            return {"errors": ["Episode not found"]}, 404

        # Check if the referenced guest exists
        guest = Guest.query.get(guest_id)
        if not guest:
            return {"errors": ["Guest not found"]}, 404

        # Create a new appearance record
        appearance = Appearance(
            rating=rating,
            episode_id=episode_id,
            guest_id=guest_id
        )

        # Add and commit the new appearance to the database
        db.session.add(appearance)
        db.session.commit()

        # Prepare response data for the newly created appearance
        response_data = {
            "id": appearance.id,
            "rating": appearance.rating,
            "guest_id": appearance.guest_id,
            "episode_id": appearance.episode_id,
            "episode": {
                "id": episode.id,
                "date": episode.date,
                "number": episode.number
            },
            "guest": {
                "id": guest.id,
                "name": guest.name,
                "occupation": guest.occupation
            }
        }

        return response_data, 201  # Return the created appearance data with a 201 (Created) status

# =====================================================================
# Adding Resources to Api
# =====================================================================
# Register resources with their endpoints
api.add_resource(EpisodeList, '/episodes')            # GET /episodes
api.add_resource(EpisodeDetail, '/episodes/<int:id>') # GET /episodes/<id>
api.add_resource(GuestList, '/guests')                # GET /guests
api.add_resource(AppearanceCreate, '/appearances')    # POST /appearances


