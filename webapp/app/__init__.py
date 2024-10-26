from flask import Flask
from .routes import main # Importerer blueprint fra routes.py
from .lock import lock # importerer blueprint fra lock.py
from .auth import auth # Importerer blueprint fra auth.py

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '\xa2|\xb1\x80\xb94D\xca*\xfd\xceP\xdf\x1d\xfe<F\xea\x0b\x85\xc3\xe7r\xf4'  # Hemmelig nøkkel krevd for flask-funksjonalitet og sikkerhet
    app.config['JSON_AS_ASCII'] = False  # Hindrer encoding av norske bokstaver til ASCII
    
    # Registrerer blueprints
    app.register_blueprint(main)
    app.register_blueprint(lock)
    app.register_blueprint(auth)

    return app
