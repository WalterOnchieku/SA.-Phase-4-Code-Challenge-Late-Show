from app import db  
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import CheckConstraint

#===========================================================================================

# Episode model represents individual episodes in the database
class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(64), nullable=False)  # Stores the date of the episode
    number = db.Column(db.Integer)  # Stores the episode number

    # Serializer rule to prevent infinite recursion with relationships
    serialize_rules = ('-episodes',)

    # Relationship to Appearance model; cascading deletes ensure associated appearances are deleted if an episode is deleted
    appearances = db.relationship('Appearance', backref='episode', cascade="all, delete", lazy=True)

    # Many-to-many relationship with Guest through the Appearance association table
    guests = db.relationship('Guest', secondary='appearances', back_populates='episodes')

    def __repr__(self):
        return f"<Episode {self.date}, {self.number}>"

#===========================================================================================

# Guest model represents guests in the database
class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)  # Guest name
    occupation = db.Column(db.String(256), nullable=False)  # Guest occupation

    # Serializer rule to prevent infinite recursion with relationships
    serialize_rules = ('-episodes',)

    # Relationship to Appearance model; cascading deletes ensure associated appearances are deleted if a guest is deleted
    appearances = db.relationship('Appearance', backref='guest', cascade="all, delete", lazy=True)

    # Many-to-many relationship with Episode through the Appearance association table
    episodes = db.relationship('Episode', secondary='appearances', back_populates='guests')

    def __repr__(self):
        return f"<Guest {self.name}, {self.occupation}>"

#===========================================================================================

# Appearance model represents an association between an Episode and a Guest, including the guest's rating of the episode
class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # Stores the rating of the appearance (must be between 1 and 5)

    # Foreign keys to Episode and Guest with cascading delete to maintain referential integrity
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id', ondelete='CASCADE'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id', ondelete='CASCADE'), nullable=False)

    # Constraint to enforce rating values between 1 and 5
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_between_1_and_5'),
    )

    def __repr__(self):
        return f"<Appearance rating={self.rating}>"

#===========================================================================================
