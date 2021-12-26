from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from dluapp import db
from sqlalchemy.sql import func
from datetime import datetime

def generate_uuid():
    return str(uuid.uuid4())

class Account(db.Model, UserMixin):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Varchar(length=35))
    password = db.Column(db.Text)
    gm_level = db.Column(db.Integer)
    locked = db.Column(db.SmallInteger)
    banned = db.Column(db.SmallInteger)
    play_key_id = db.Column(db.Integer)
    created_at = db.Column(db.Timestamp)
    mute_expire = db.Column(db.BigInteger(20))
    email = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def get_id(self):
           return (self.uid)

    def __repr__(self):
        return '<User {}>'.format(self.email)
    def __str__(self):
        return '<{}>'.format(self.email)

class Radio(db.Model):
    __tablename__ = 'radio'
    rid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    createDate = db.Column(db.DateTime, server_default=func.now())
    lastModifiedDate = db.Column(db.DateTime, server_default=func.now(), onupdate=func.current_timestamp())
    online = db.Column(db.Boolean)
    lastHeard = db.Column(db.DateTime)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    alt = db.Column(db.Float)
    head = db.Column(db.Float)
    vel = db.Column(db.Float)
    pings = db.relationship('RadioCheckin', backref='radio', lazy=True)
    locs = db.relationship('RadioLocation', backref='radio', lazy=True)
    calls = db.relationship('Call', backref='radio', lazy=True)

    def __repr__(self):
        return '<Radio {}>'.format(self.rid)
    def __str__(self):
        return '<{}>'.format(self.name)
    def serialize(self):
        return {"rid": self.rid,
                "name": self.name,
                "createDate": self.createDate,
                "lastModifiedDate": self.lastModifiedDate,
                "online": self.online,
                "lastHeard": self.lastHeard,
                "lat": self.lat,
                "lon": self.lon,
                "alt": self.alt,
                "head": self.head,
                "vel": self.vel}
