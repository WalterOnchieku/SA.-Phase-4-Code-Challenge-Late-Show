
from app import db  
from sqlalchemy_serializer import SerializerMixin

#===========================================================================================

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(64), nullable=False)
    number = db.Column(db.Integer)

    # Specify serialization rules to limit recursion depth here
    serialize_rules = ('-episodes',)

    # Relationship to `Appearance` and backref to `Episode`
    appearances = db.relationship('Appearance', backref='episode', cascade="all, delete", lazy=True)

    # Relationship to `Guest` through `Appearance`
    guests = db.relationship('Guest', secondary='appearances', back_populates='episodes')

    def __repr__(self):
        return f"<Episode {self.date}, {self.number}>"

#===========================================================================================

class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    occupation = db.Column(db.String(256), nullable=False)  

    # Specify serialization rules to limit recursion depth here
    serialize_rules = ('-episodes',)

    # Relationship to `Appearance` and backref to `Guest`
    appearances = db.relationship('Appearance', backref='guest', cascade="all, delete", lazy=True)

    # Relationship to `Episode` through `Appearance`
    episodes = db.relationship('Episode', secondary='appearances', back_populates='guests')

    def __repr__(self):
        return f"<Guest {self.name}, {self.occupation}>"

#===========================================================================================

from sqlalchemy import CheckConstraint

class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    # Foreign keys with cascading deletes
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id', ondelete='CASCADE'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id', ondelete='CASCADE'), nullable=False)

    # Add the CheckConstraint for rating
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_between_1_and_5'),
    )

    def __repr__(self):
        return f"<Appearance rating={self.rating}>"


#===========================================================================================