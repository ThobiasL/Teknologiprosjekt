import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '\xa2|\xb1\x80\xb94D\xca*\xfd\xceP\xdf\x1d\xfe<F\xea\x0b\x85\xc3\xe7r\xf4'
    JSON_AS_ASCII = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../data/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Unngå unødvendige advarsler