import pytest
from application import create_app
from adapters.database import db
from application.config import TestConfig
from werkzeug.security import generate_password_hash
from core.models.user import User
from core.models.autodoorlock import AutoDoorLock
from core.models.medication import Medication

@pytest.fixture
def app():
    app = create_app(TestConfig)  # Opprett en testapp
    with app.app_context():
        db.create_all()
        yield app  # Leverer appen til testene
        db.session.remove()
        db.drop_all()
        db.session.close()

# Fixture for å hente en testklient
@pytest.fixture
def client(app):
    return app.test_client()

# Fixture for å hente en test CLI runner
@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# Legger til testdata i memory-databasen til testene
@pytest.fixture
def init_data(app):

    with app.app_context():
        user1 = User(name='test_user1', password_hash=generate_password_hash('password1'))
        user2 = User(name='test_user2', password_hash=generate_password_hash('password2'))
        autodoorlock = AutoDoorLock(time=None, status=False)
        medication = Medication(time=None)

        db.session.add_all([user1, user2, autodoorlock, medication])
        db.session.commit()

# Login-funksjon for å logge inn brukere før testene
@pytest.fixture
def login(client, app):
    def _login(name, password):
        with app.app_context():
            user = User.query.filter_by(name=name).first()
        response = client.post('/login', data={'id': user.id, 'password': password})
        assert response.status_code == 302
        assert '/home' in response.location
        return response
    return _login