from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    db.drop_all()
    db.create_all()

class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(20), primary_key=True, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    #TODO implement logic surrounding is_admin column

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        hashed_password = bcrypt.generate_password_hash(password) 
        hashed_password_utf8 = hashed_password.decode("utf8")
        return cls(username=username, password=hashed_password_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return False

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)
    created_at = db.Column(db.Date, default=db.func.current_timestamp())