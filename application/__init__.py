from flask import Flask, session, request, redirect, url_for # Importerer nødvendige funksjoner fra Flask
from application.database import db # Importerer databasen

from .config import Config # Importerer konfigurasjon fra config.py

# Importerer modeller
from adapters.database.flask.user_flask import User
from adapters.database.flask.autodoorlock_flask import AutoDoorLock
from adapters.database.flask.medication_flask import Medication
from adapters.database.flask.task_flask import Task

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
        if 'user_id' not in session and request.endpoint not in exempt_routes:
            return redirect(url_for('auth.login'))

    with app.app_context():
        db.create_all()  # Oppretter tabeller i databasen

    return app