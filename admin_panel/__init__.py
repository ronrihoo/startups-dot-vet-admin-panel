import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


basedir = os.path.abspath(os.path.dirname(__file__))


# App
app = Flask(__name__)
app.config['DEBUG'] = True


# Database
app.config['SECRET_KEY'] = '\xd7\x0e\xddSA\xc5o\xe7|d\xf3\xfe\xe9o+\x17\xed_}2\xb4\x9a\xc3\xc4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'adminpanel.db')
db = SQLAlchemy(app)
# db_user = 'admin'
# db_pass = 't3$T_p4SS'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + 'admin:10' + \
#                                         '/' + os.path.join(basedir, 'startups.db')


# Authentication
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)


import models
import views