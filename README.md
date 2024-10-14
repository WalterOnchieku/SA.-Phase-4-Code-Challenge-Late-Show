# Episode-Guest Appearance API

A simple Flask-based REST API to manage TV show episodes, guests, and their appearances. This API supports CRUD operations for `Episodes`, `Guests`, and `Appearances`.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Setup](#database-setup)
- [API Endpoints](#api-endpoints)
  - [Episodes](#episodes)
  - [Guests](#guests)
  - [Appearances](#appearances)
- [Seeding the Database](#seeding-the-database)
- [Running the App](#running-the-app)

---

## Features

- **Episode Management**: Add, view, and retrieve episodes.
- **Guest Management**: View and retrieve guest information.
- **Appearances**: Track guest appearances with ratings linked to episodes.
- **Seeding**: Easily seed your database using a CSV file.

---

## Technologies

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- SQLite (default database)
- SQLAlchemy Serializer

---

## Getting Started

### Prerequisites

- Python 3.8+
- `pip` (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/episode-guest-api.git
   cd episode-guest-api

2. **Create a virtual environment (optional but recommended):**

```bash
Copy code
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows

3. Install dependencies:

bash
Copy code
pip install -r requirements.txt
Database Setup
The project uses SQLite as its database. To initialize the database, run:

bash
Copy code
python
>>> from app import db, create_app
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
This will create the necessary tables for Episodes, Guests, and Appearances.

API Endpoints

Episodes
GET /episodes
Retrieves all episodes.

GET /episodes/
Retrieves a specific episode with its appearances and associated guest details.


Guests
GET /guests
Retrieves all guests.


Appearances
POST /appearances
Creates a new appearance that associates an existing episode and guest.


Seeding the Database
To seed the database with data from a CSV file, you can use the /seed endpoint after setting up the app.

Place your CSV file in the project directory and name it accordingly (e.g., seed.csv).

Ensure the seed route is set up (you may need to define one in routes.py).
Run the app, and send a POST request to /seed to populate the database with data from the file.
Running the App
To start the Flask app:

bash
Copy code
python routes.py
The app will run locally at http://127.0.0.1:5000/. You can now test the API using Postman, cURL, or any other API client.

