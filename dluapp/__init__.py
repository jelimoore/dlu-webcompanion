from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import logging

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

from dluapp import base_routes, user_routes, admin_routes, models
