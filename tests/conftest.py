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
        user = User(name='test_user', password_hash=generate_password_hash('password'))
        user2 = User(name='test_user2', password_hash=generate_password_hash('password2'))
        autodoorlock = AutoDoorLock(time=None, status=False)
        medication = Medication(
            day='Monday', dose_1=None, dose_2=None, dose_3=None, dose_4=None,
            scheduled_1=False, scheduled_2=False, scheduled_3=False, scheduled_4=False
        )
        task = Task(name='Medisin', time=None, scheduled=False)

        db.session.add_all([user, user2, autodoorlock, medication, task])
        db.session.commit()

# Login-funksjon for å logge inn brukere før tester
@pytest.fixture
def login(client, app):
    def _login(name, password):
        with app.app_context():
            user = User.query.filter_by(name=name).first()
            assert user is not None, f"Bruker '{name}' finnes ikke i db."

        response = client.post('/login', data={'id': user.id, 'password': password})
        assert response.status_code == 302, "Bruker ble ikke videresendt."
        assert '/home' in response.location, "Bruker ble ikke videresendt til hjemmesiden."

        with client.session_transaction() as session:
            assert 'user_id' in session, "Bruker ble ikke lagt til i session."

        return response
    
    return _login