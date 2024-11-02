from flask import Flask, session, request, redirect, url_for # Importerer nødvendige funksjoner fra Flask

from .config import Config # Importerer konfigurasjon fra config.py

from adapters.database import db  # Importerer databasemodulen

# Importerer modeller
from core.models.user import User
from core.models.autodoorlock import AutoDoorLock
from core.models.autopilldispenser import AutoPillDispenser

# Importerer blueprints fra deres respektive filer
from .routes.main import main
from .routes.autodoorlock import autodoorlock
from .routes.auth import auth
from .routes.medication import medication

def create_app():
    app = Flask(__name__) # Lager en Flask-app
    app.config.from_object(Config)  # Henter konfigurasjon fra config.py
    
    db.init_app(app)  # Initialiserer databasen
    # Registrerer blueprints
    app.register_blueprint(main)
    app.register_blueprint(autodoorlock)
    app.register_blueprint(auth)
    app.register_blueprint(medication)

    # Funksjon for å sjekke autentisering før hver request, ved å sjekke om brukernavn er i session
    @app.before_request
    def check_auth():
        
        exempt_routes = ['auth.login', 'auth.register', 'static']

        if 'username' not in session and request.endpoint not in exempt_routes:
            return redirect(url_for('auth.login'))
        
    with app.app_context():
        db.create_all()  # Oppretter databasetabeller

    return app