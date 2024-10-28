
from flask_restful import Resource
from models import Episode, Guest, Appearance

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# GET /episodes - Retrieve list of episodes
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Episode_List_Resource(Resource):
    def get(self):
        episodes = Episode.query.all()
        episodes_list = [episode.to_dict(only=('id', 'date', 'number')) for episode in episodes]
        return episodes_list, 200


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# GET /episodes/<id> - Retrieve specific episode details with appearances
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Episode_Detail_Resource(Resource):
    def get(self, id):
        episode = Episode.query.get(id)
        
        if not episode:
            return {"error": "Episode not found"}, 404
        
        # Serialize episode with nested appearances and guest details
        episode_data = episode.to_dict(only=('id', 'date', 'number'))
        episode_data['appearances'] = [
            {
                "id": appearance.id,
                "rating": appearance.rating,
                "episode_id": appearance.episode_id,
                "guest_id": appearance.guest_id,
                "guest": appearance.guest.to_dict(only=("id", "name", "occupation"))
            } for appearance in episode.appearances
        ]
        
        return episode_data, 200

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# GET /guests - Retrieve list of guests
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Guest_List_Resource(Resource):
    def get(self):
        guests = Guest.query.all()
        guests_data = [guest.to_dict(only=("id", "name", "occupation")) for guest in guests]
        return guests_data, 200

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# POST /appearances - Create a new appearance
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Appearance_Create_Resource(Resource):
    def post(self):
        data = request.get_json()

        # Validate required fields
        rating = data.get("rating")
        episode_id = data.get("episode_id")
        guest_id = data.get("guest_id")

        if not (rating and episode_id and guest_id):
            return {"errors": ["All fields (rating, episode_id, guest_id) are required."]}, 400

        # Validate rating range
        if not (1 <= rating <= 5):
            return {"errors": ["Rating must be between 1 and 5."]}, 400

        # Retrieve Episode and Guest to ensure they exist
        episode = Episode.query.get(episode_id)
        guest = Guest.query.get(guest_id)

        if not episode or not guest:
            return {"errors": ["Episode or Guest not found."]}, 404

        # Create and save the new Appearance instance
        new_appearance = Appearance(rating=rating, episode_id=episode_id, guest_id=guest_id)
        db.session.add(new_appearance)
        db.session.commit()

        # Return serialized response data
        appearance_data = new_appearance.to_dict(only=("id", "rating", "guest_id", "episode_id"))
        appearance_data["episode"] = episode.to_dict(only=("id", "date", "number"))
        appearance_data["guest"] = guest.to_dict(only=("id", "name", "occupation"))
        
        return appearance_data, 201