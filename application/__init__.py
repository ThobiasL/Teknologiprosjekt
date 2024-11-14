from flask import Flask, session, request, redirect, url_for # Importerer nødvendige funksjoner fra Flask
from application.database import db # Importerer databasen

from .config import Config # Importerer konfigurasjon fra config.py

# Importerer modeller
from adapters.database.user_db import User
from adapters.database.autodoorlock_db import AutoDoorLock
from adapters.database.medication_db import Medication
from adapters.database.task_db import Task

# Importerer blueprints
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

    # Før hver request nullstilles flash-meldinger, og brukerautentisering sjekkes
    @app.before_request
    def before_request():
        exempt_routes = ['auth.login', 'auth.register', 'static']
        if 'username' not in session and request.endpoint not in exempt_routes:
            return redirect(url_for('auth.login'))

    with app.app_context():
        db.create_all()  # Oppretter databasetabeller

    return app