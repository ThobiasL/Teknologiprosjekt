import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.urandom(24) # Setter en tilfeldig secret key på 24 bytes
    JSON_AS_ASCII = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../data/database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Unngå unødvendige advarsler
    SKIP_AUTH = False # Setter autentisering til å være på som default