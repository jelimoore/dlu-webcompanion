from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from dluapp import db
from sqlalchemy.sql import func
from datetime import datetime
from bcrypt import checkpw, hashpw, gensalt

class Account(db.Model, UserMixin):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=35))
    password = db.Column(db.Text)
    gm_level = db.Column(db.Integer)
    locked = db.Column(db.SmallInteger)
    banned = db.Column(db.SmallInteger)
    play_key_id = db.Column(db.Integer, db.ForeignKey('play_keys.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    mute_expire = db.Column(db.BigInteger())
    email = db.Column(db.String(256))

    def set_password(self, password):
        self.password = hashpw(password.encode('utf-8'), gensalt(prefix=b"2a"))
    def check_password(self, password):
        return checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    def get_id(self):
        return (self.id)
    def __repr__(self):
        return '<User {}>'.format(self.email)
    def __str__(self):
        return '<{}>'.format(self.email)

class BugReport(db.Model):
    __tablename__ = 'bug_reports'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    client_version = db.Column(db.Text)
    other_player_id = db.Column(db.Text)
    selection = db.Column(db.Text)
    submitted = db.Column(db.DateTime)

class Character(db.Model):
    __tablename__ = 'charinfo'
    id = db.Column(db.BigInteger, primary_key=True)
    account_id = db.Column(db.Integer)
    name = db.Column(db.String(35))
    pending_name = db.Column(db.String(35))
    needs_rename = db.Column(db.SmallInteger)
    prop_clone_id = db.Column(db.BigInteger)
    last_login = db.Column(db.BigInteger)
    permission_map = db.Column(db.BigInteger)

    # ORM backrefs
    characterData = db.relationship('CharacterData', backref='charinfo', lazy=True)


class CharacterData(db.Model):
    __tablename__ = 'charxml'
    id = db.Column(db.BigInteger, db.ForeignKey('charinfo.id'), nullable=False, primary_key=True)
    xml_data = db.Column(db.Text)

class Leaderboard(db.Model):
    __tablename__ = 'leaderboard'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer)
    last_played = db.Column(db.DateTime)
    character_id = db.Column(db.BigInteger, db.ForeignKey('charinfo.id'), nullable=False)
    time = db.Column(db.BigInteger)
    score = db.Column(db.BigInteger)

    #ORM backrefs
    character = db.relationship('Character', backref='charinfo', lazy=True)


class PlayKey(db.Model):
    __tablename__ = 'play_keys'
    id = db.Column(db.Integer, primary_key=True)
    key_string = db.Column(db.String(19))
    key_uses = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    active = db.Column(db.SmallInteger)
    claimed_by = db.Column(db.String(255))

    # ORM backrefs
    account = db.relationship('Account', backref='play_keys', lazy=True)
