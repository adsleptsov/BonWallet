import os
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PARENT_DIR, 'main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy()
