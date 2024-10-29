from run import app
# from app import app
from models import db, Episode, Guest, Appearance
from sqlalchemy import text

with app.app_context():
    print('Deleting existing episodes, guests, and appearances...')
    db.session.execute(text('DELETE FROM appearances;'))  # Clear appearances table
    db.session.execute(text('DELETE FROM guests;'))       # Clear guests table
    db.session.execute(text('DELETE FROM episodes;'))     # Clear episodes table

    print('Creating episode objects...')
    episode1 = Episode(date='2024-01-01', number=1)
    episode2 = Episode(date='2024-01-08', number=2)
    episode3 = Episode(date='2024-01-15', number=3)
    episode4 = Episode(date='2024-01-22', number=4)

    print('Creating guest objects...')
    guest1 = Guest(name='Alice Smith', occupation='Actress')
    guest2 = Guest(name='Bob Johnson', occupation='Musician')
    guest3 = Guest(name='Charlie Brown', occupation='Comedian')
    guest4 = Guest(name='Diana Prince', occupation='Writer')

    print('Adding episode objects to transaction...')
    db.session.add_all([episode1, episode2, episode3, episode4])

    print('Adding guest objects to transaction...')
    db.session.add_all([guest1, guest2, guest3, guest4])

    print('Committing episodes and guests transaction...')
    db.session.commit()

    print('Creating appearance objects...')
    appearance1 = Appearance(rating=5, episode_id=1, guest_id=1)  # Episode 1, Alice Smith
    appearance2 = Appearance(rating=4, episode_id=1, guest_id=2)  # Episode 1, Bob Johnson
    appearance3 = Appearance(rating=3, episode_id=2, guest_id=1)  # Episode 2, Alice Smith
    appearance4 = Appearance(rating=2, episode_id=3, guest_id=3)  # Episode 3, Charlie Brown
    appearance5 = Appearance(rating=5, episode_id=4, guest_id=4)  # Episode 4, Diana Prince
    appearance6 = Appearance(rating=4, episode_id=4, guest_id=2)  # Episode 4, Bob Johnson

    print('Adding appearance objects to transaction...')
    db.session.add_all([appearance1, appearance2, appearance3, appearance4, appearance5, appearance6])

    print('Committing appearance transaction...')
    db.session.commit()

    print('Complete.')
