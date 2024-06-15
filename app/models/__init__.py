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


class Venue( db.Model):
    __tablename__ = "venue"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    place = db.Column(db.String(64), nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    shows = db.relationship('Show',
                                    foreign_keys='Show.venue_id',
                                    backref='venue', lazy='dynamic')

    def __repr__(self):
        return '<Venue {}>'.format(self.name)
    


class Show( db.Model):
    __tablename__ = "show"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    tags = db.Column(db.String(64))
    price = db.Column(db.Integer, nullable=False, default=0)
    date_from = db.Column(db.Date)
    date_to   = db.Column(db.Date)
    timing = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    
    images = db.relationship("Images", back_populates="show")
    bookings = db.relationship("Booking", back_populates="show")

    def __repr__(self):
        return '<Show {}>'.format(self.name)
    
    @hybrid_property
    def schedules(self):
        tmp = self.timing.split(',')
        s = {}
        for t in tmp:
            dt = datetime.fromtimestamp(int(t)/1000)
            
            if dt.strftime("%d/%m/%y") not in s:
                s[dt.strftime("%d/%m/%y")] = list()

            s[dt.strftime("%d/%m/%y")].append(dt.strftime("%H:%M"))    
            
        return s
    
    @hybrid_property
    def main_image(self):
        return url_for('static', filename='image/'+ self.images[0].path )
    
    @hybrid_property
    def place(self):
        return self.venue
    
    def json(self):
        return {'id': self.id,'name': self.name, 'price': self.price, 'image': self.main_image, 's': self.schedules}

class Images(db.Model):
    __tablename__ = "image"
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(64), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    show = db.relationship("Show", back_populates="images")

def json(self):
    return {'id': self.id, 'path': self.path}

def to_dict(self):
    keys = self.__mapper__.attrs.keys()
    attrs = vars(self)
    return { k : attrs[k]  for k in keys}


class Booking( db.Model):
    __tablename__ = "booking"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    showTime = db.Column(db.String(255), nullable=False)
    sheats = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    show = db.relationship("Show", back_populates="bookings")

    def __repr__(self):
        return '<Show {}>'.format(self.date, self.showTime)   