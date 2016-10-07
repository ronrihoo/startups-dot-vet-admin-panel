from datetime import datetime

from sqlalchemy import desc
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from admin_panel import db


class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    url = db.Column(db.Text)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    count = db.Column(db.Integer)
    diff = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    @staticmethod
    def recent(num):
        return Scan.query.order_by(desc(Scan.datetime)).limit(num)

    @staticmethod
    def last_scan(name):
        return Scan.query.filter(Scan.name == name).order_by(desc(Scan.datetime)).limit(1)

    def __repr__(self):
        return "Invoked {} scanner at {}".format(self.name, self.datetime)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String)
    email = db.Column(db.String(120), unique=True)
    scans = db.relationship('Scan', backref='user', lazy='dynamic')

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '{}'.format(self.username)
