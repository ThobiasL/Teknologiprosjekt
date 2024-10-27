from flask import Flask, session, request, redirect, url_for
# Importerer blueprints fra deres respektive filer
from .routes import main
from .lock import lock
from .auth import auth
from .medication import medication

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '\xa2|\xb1\x80\xb94D\xca*\xfd\xceP\xdf\x1d\xfe<F\xea\x0b\x85\xc3\xe7r\xf4'  # Hemmelig nøkkel krevd for flask-funksjonalitet og sikkerhet
    app.config['JSON_AS_ASCII'] = False  # Hindrer encoding av eventuelle norske bokstaver til ASCII
    
    # Registrerer blueprints
    app.register_blueprint(main)
    app.register_blueprint(lock)
    app.register_blueprint(auth)
    app.register_blueprint(medication)

    @app.before_request
    def check_auth():
        
        exempt_routes = ['auth.login', 'auth.register', 'static']

        if request.endpoint not in exempt_routes and 'username' not in session:
            return redirect(url_for('auth.login'))

    return app