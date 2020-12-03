from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pickle
from embedding_as_service_client import EmbeddingClient

db = SQLAlchemy()
migrate = Migrate()

en = EmbeddingClient(host='54.180.124.154', port=8989)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    full_name = db.Column(db.String, nullable=False)
    followers = db.Column(db.Integer, default=0)
    location = db.Column(db.String)

    def __repr__(self):
        return f"<User {self.id} {self.username}>"


class Tweet(db.Model):
    __tablename__ = 'tweet'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    user = db.relationship('User',backref=db.backref('tweets', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    embedding = db.Column(db.PickleType)

    def __repr__(self):
        return f"<Tweet {self.id}>"

def get_userdata():
    return User.query.all()

def set_tweetdata():
    user = User.query.get(twitter_user.id) or User(id=twitter_user.id)

    db.session.add(user)
    db.session.commit()
    
    return Tweet.query.all()