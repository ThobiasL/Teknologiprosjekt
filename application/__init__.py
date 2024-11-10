from flask import Flask, session, request, redirect, url_for, flash, get_flashed_messages # Importerer nødvendige funksjoner fra Flask
from application.database import db # Importerer databasen

from .config import Config # Importerer konfigurasjon fra config.py

# Importerer modeller
from core.models.user import User
from core.models.autodoorlock import AutoDoorLock
from core.models.medication import Medication
from core.models.task import Task

# Importerer blueprints fra deres respektive filer
from adapters.http.main import main
from adapters.http.autodoorlock import autodoorlock
from adapters.http.auth import auth
from adapters.http.medication import medication
from adapters.http.tasks import tasks

def create_app(config=None):
    app = Flask(__name__) # Lager en Flask-app
    
    if config:
        app.config.from_object(config)
    else:
        app.config.from_object(Config)
    
    db.init_app(app)  # Initialiserer databasen
    # Registrerer blueprints
    app.register_blueprint(main)
    app.register_blueprint(autodoorlock)
    app.register_blueprint(auth)
    app.register_blueprint(medication)
    app.register_blueprint(tasks)

    # Funksjon for å sjekke autentisering
    @app.before_request
    def check_auth():
        # Sjekker om autentisering skal hoppes over, med standardverdi False
        if app.config.get('SKIP_AUTH', False):
            session['username'] = 'Admin' # Setter brukernavn til Admin for å gi tilgang til alle sider
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