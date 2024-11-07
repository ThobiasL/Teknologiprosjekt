import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.urandom(24) # Setter en tilfeldig secret key på 24 bytes
    JSON_AS_ASCII = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../data/database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Unngå unødvendige advarsler
    SKIP_AUTH = False # Setter autentisering til å være på som default

class DevConfig(Config):
    SKIP_AUTH = True # Setter autentisering til å være av for utvikling
    DEBUG = True # Setter debug til å være på for utvikling

class TestConfig(Config):
    TESTING = True # Setter testing til å være på
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # Bruker en midlertidig database i minnet for testing
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Unngå unødvendige advarsler