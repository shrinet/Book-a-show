from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from app import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import UserMixin, RoleMixin
from datetime import datetime, timedelta
from flask import session, url_for




class User(UserMixin, db.Model):
    __tablename__ = "user"
    id=db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    email=db.Column(db.String(64), nullable=False,unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    fullname=db.Column(db.String(64),nullable=True)
    password_hash=db.Column(db.String(64), nullable=False)
    userType = db.Column(db.String(20), default = 'user')
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=True)
    bookings = db.relationship('Booking', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @hybrid_property
    def isAdmin(self): #an example method - your admin view could use this method to check if a user should be given access
         if self.userType == 'admin':
             return True
         else:
             return False
         
    def avatar(self, size):
        digest = self.email.lower().encode('utf-8')
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)     
         
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return self.id

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
        
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    

       

class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(64), nullable=False)