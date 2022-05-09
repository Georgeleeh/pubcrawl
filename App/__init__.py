from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



application = Flask(__name__)
application.config.from_object(Config)

db = SQLAlchemy(application)

from App import routes
from App import models

db.create_all()