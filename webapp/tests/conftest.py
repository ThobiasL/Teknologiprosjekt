import os
import pytest
from webapp.app import create_app
from webapp.adapters.database import db
from webapp.app.config import TestConfig
from werkzeug.security import generate_password_hash
from webapp.core.models.user import User

@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(TestConfig)

    with app.app_context():
        db.create_all() # Oppretter databasetabeller før testen starter
        yield app # Leverer appen til testen
        db.session.remove()
        db.drop_all() # Dropper databasetabeller etter testen er ferdig

# Fixture for å hente en testklient
@pytest.fixture
def client(app):
    return app.test_client()

# Fixture for å hente en test CLI runner
@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# Legger til testdata til testene
@pytest.fixture
def init_data(app):


    # Legger til testbrukere
    user1 = User(name='test_user1', password_hash=generate_password_hash('password1'))
    user2 = User(name='test_user2', password_hash=generate_password_hash('password2'))
    db.session.add_all([user1, user2])
    db.session.commit()

    return user1, user2 # Returnerer brukerne for å kunne bruke de i testene
