from flask import Flask
from .routes import main # Importerer blueprint fra routes.py
from .lock import lock # importerer blueprint fra lock.py

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey123123' # midlertidig nøkkel til sessions
    app.config['JSON_AS_ASCII'] = False  # Hindrer encoding av norske bokstaver til ASCII
    
    # Registrer Blueprint med routes
    app.register_blueprint(main)
    app.register_blueprint(lock)

    return app
