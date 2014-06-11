from app import db

# Add database model to store user_id, user_key and user_secret
# Used for accessing API


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=True)
    user_key = db.Column(db.String(120), unique=True)
    user_secret = db.Column(db.String(120), unique=True)

    def __init__(self, user_id, user_key, user_secret):
        self.user_id = user_id
        self.user_key = user_key
        self.user_secret = user_secret

    def __repr__(self):
        return '<User %r>' % self.user_id
