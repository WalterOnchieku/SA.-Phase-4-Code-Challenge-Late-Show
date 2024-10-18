### Flask Show Guest API
This is a simple Flask application that manages episodes, guests, and their appearances on a show. It uses SQLAlchemy for database management, Flask-Migrate for database migrations, and includes RESTful API endpoints for CRUD operations on episodes, guests, and appearances.

## Features 
Episodes: Manage show episodes (date and number).
Guests: Manage guest information (name and occupation).
Appearances: Track which guests appeared in which episodes, along with a rating.
Database: Uses SQLite (can be configured for other databases) and SQLAlchemy for ORM.
API Endpoints: Provides RESTful API routes for managing episodes, guests, and appearances.

### Table of Contents
- Requirements
- Setup
- Database Migrations
- API Endpoints


***Requirements***
1. Python 3.x
2. Flask
3. Flask-SQLAlchemy
4. Flask-Migrate
5. sqlalchemy_serializer
6. Setup

Clone the repository:

```bash
Copy code
git clone <https://github.com/WalterOnchieku/SA.-Phase-4-Code-Challenge-Late-Show>
cd <repository-folder>
```
Create and activate a virtual environment:

```bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install dependencies:

```bash
Copy code
pip install -r requirements.txt
```
Set up the SQLite database:

```bash
Copy code
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

Run the Flask app:

```bash
Copy code
flask run
```
The app will be running locally on http://127.0.0.1:5555/.

## Database Migrations
After making any changes to the models, run the following commands to apply migrations:

```bash
Copy code
flask db migrate -m "Describe your migration"
flask db upgrade
```
## API Endpoints
Episodes
GET /episodes: Get a list of all episodes.
GET /episodes/
: Get details of a specific episode by ID.
Guests
GET /guests: Get a list of all guests.
Appearances
POST /appearances: Create a new appearance (guest appearing in an episode).
Seed Data (Optional)
If you have a CSV file (seed.csv) to seed data:

```bash
Copy code
python seed.py
```
This will load episodes, guests, and appearances from the CSV file into the database.