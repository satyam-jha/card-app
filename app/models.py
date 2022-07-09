from sqlalchemy.ext.declarative import declarative_base
from app import db

Base = declarative_base()


def to_collection_dict(query):
        data = {
            'decks': [item.to_dict() for item in query] 
            }
        return data


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'emaiil': self.email
            }
        return data

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            }
        return data

    def __repr__(self):
        return self.name

class card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(128))
    answer = db.Column(db.String(128))
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))
    order = db.Column(db.Integer)

    def to_dict(self):
        data = {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'deck': Deck.query.get_or_404(self.deck_id).to_dict(),
            'order':self.order
            }
        return data

    def __repr__(self):
        return self.question

class UserCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('deck.id'))
    last_read = db.Column(db.DateTime)




