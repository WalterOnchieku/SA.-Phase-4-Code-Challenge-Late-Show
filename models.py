
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import CheckConstraint

# Initialize db here
db = SQLAlchemy()

#===========================================================================================

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(64), nullable=False)
    number = db.Column(db.Integer)

    serialize_rules = ('-episodes',)

    appearances = db.relationship('Appearance', backref='episode', cascade="all, delete", lazy=True)
    guests = db.relationship('Guest', secondary='appearances', back_populates='episodes')

    def __repr__(self):
        return f"<Episode {self.date}, {self.number}>"

#===========================================================================================

class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    occupation = db.Column(db.String(256), nullable=False)

    serialize_rules = ('-episodes',)

    appearances = db.relationship('Appearance', backref='guest', cascade="all, delete", lazy=True)
    episodes = db.relationship('Episode', secondary='appearances', back_populates='guests')

    def __repr__(self):
        return f"<Guest {self.name}, {self.occupation}>"

#===========================================================================================

class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id', ondelete='CASCADE'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_between_1_and_5'),
    )

    def __repr__(self):
        return f"<Appearance rating={self.rating}>"

#===========================================================================================
