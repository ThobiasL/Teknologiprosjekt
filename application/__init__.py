from flask import Flask, session, request, redirect, url_for, flash, get_flashed_messages # Importerer nødvendige funksjoner fra Flask

from .config import Config # Importerer konfigurasjon fra config.py

from adapters.database import db  # Importerer databasemodulen

# Importerer modeller
from core.models.user import User
from core.models.autodoorlock import AutoDoorLock
from core.models.autopilldispenser import AutoPillDispenser

# Importerer blueprints fra deres respektive filer
from .blueprints.main import main
from .blueprints.autodoorlock import autodoorlock
from .blueprints.auth import auth
from .blueprints.medication import medication

def create_app():
    app = Flask(__name__) # Lager en Flask-app
    app.config.from_object(Config)  # Henter konfigurasjon fra config.py
    
    db.init_app(app)  # Initialiserer databasen
    # Registrerer blueprints
    app.register_blueprint(main)
    app.register_blueprint(autodoorlock)
    app.register_blueprint(auth)
    app.register_blueprint(medication)

    # Funksjon for å sjekke autentisering
    @app.before_request
    def check_auth():

        # Sjekker om autentisering skal hoppes over, med standardverdi False
        if app.config.get('SKIP_AUTH', False):
            session['username'] = 'test_user'
            return
        
        exempt_routes = ['auth.login', 'auth.register', 'static']

        # Sender brukeren til innloggingssiden hvis de ikke er logget inn, og ikke er på en side som ikke krever innlogging
        if 'username' not in session and request.endpoint not in exempt_routes:
            return redirect(url_for('auth.login'))
        
    # Funksjon for å cleare flash-meldinger
    def clear_flashed_messages():
        get_flashed_messages()

    with app.app_context():
        db.create_all()  # Oppretter databasetabeller

    return app