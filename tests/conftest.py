import pytest
from application import create_app
from application.database import db
from application.config import TestConfig
from werkzeug.security import generate_password_hash
from adapters.database.user_db import User
from adapters.database.autodoorlock_db import AutoDoorLock
from adapters.database.medication_db import Medication
from adapters.database.task_db import Task

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
        db.session.close()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def init_data(app):
    with app.app_context():
        user = User(name='test_user', password_hash=generate_password_hash('password1'))
        autodoorlock = AutoDoorLock(time=None, status=False)
        medication = Medication(
            day='Mandag', dose_1=None, dose_2=None, dose_3=None, dose_4=None,
            scheduled_1=False, scheduled_2=False, scheduled_3=False, scheduled_4=False
        )
        task = Task(name='Medisin', time=None, scheduled=False)

        db.session.add_all([user, autodoorlock, medication, task])
        db.session.commit()

# Login-funksjon for å logge inn brukere før tester
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