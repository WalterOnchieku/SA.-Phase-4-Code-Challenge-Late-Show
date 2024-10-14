from flask import Flask, jsonify, request
from models import Episode, Guest, Appearance
from app import db, create_app

# Initialize the Flask app
app = create_app()

# =====================================================================
# Route: GET /episodes
# =====================================================================
@app.route('/episodes', methods=['GET'])
def get_episodes():
    # Query all Episode records
    episodes = Episode.query.all()
    
    # Convert the result into a list of dictionaries
    episode_list = [
        {
            "id": episode.id,
            "date": episode.date,
            "number": episode.number
        }
        for episode in episodes
    ]
    
    # Return the JSON response
    return jsonify(episode_list), 200

# =====================================================================
# Route: GET /episodes/:id
# =====================================================================
@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    # Fetch the Episode by ID
    episode = Episode.query.get(id)

    if not episode:
        # If the episode doesn't exist, return a 404 error
        return jsonify({"error": "Episode not found"}), 404

    # If episode exists, prepare the response data
    episode_data = {
        "id": episode.id,
        "date": episode.date,
        "number": episode.number,
        "appearances": []
    }

    # Fetch associated appearances for this episode
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

    # Return the episode data as JSON
    return jsonify(episode_data), 200

# =====================================================================
# Route: GET /guests
# =====================================================================
@app.route('/guests', methods=['GET'])
def get_guests():
    # Query all Guest records
    guests = Guest.query.all()
    
    # Convert the result into a list of dictionaries
    guest_list = [
        {
            "id": guest.id,
            "name": guest.name,
            "occupation": guest.occupation
        }
        for guest in guests
    ]
    
    # Return the JSON response
    return jsonify(guest_list), 200

# =====================================================================
# Route: POST /appearances
# =====================================================================
@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()

    # Validate required fields
    rating = data.get('rating')
    episode_id = data.get('episode_id')
    guest_id = data.get('guest_id')

    # Validate that rating is between 1 and 5
    if not (1 <= rating <= 5):
        return jsonify({"errors": ["Rating must be between 1 and 5"]}), 400

    # Check if the episode exists
    episode = Episode.query.get(episode_id)
    if not episode:
        return jsonify({"errors": ["Episode not found"]}), 404

    # Check if the guest exists
    guest = Guest.query.get(guest_id)
    if not guest:
        return jsonify({"errors": ["Guest not found"]}), 404

    # Create new appearance
    appearance = Appearance(
        rating=rating,
        episode_id=episode_id,
        guest_id=guest_id
    )
    
    # Add and commit to the database
    db.session.add(appearance)
    db.session.commit()

    # Prepare the response data
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

    # Return the created appearance data
    return jsonify(response_data), 201

# =====================================================================
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# =====================================================================

if __name__ == '__main__':
    app.run(debug=True)
