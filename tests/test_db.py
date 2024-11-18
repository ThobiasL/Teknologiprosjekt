# Enhetstester for enkle databaseoperasjoner

import pytest
from application.database import db
from adapters.database.user_db import User
from adapters.database.medication_db import Medication
from adapters.database.models.autodoorlock_db import AutoDoorLock

# Fixture for å opprette en bruker i testdatabasen
@pytest.fixture
def create_user():
    user = User(name='test_user', password_hash='hash')
    db.session.add(user)
    db.session.commit()
    yield user
    db.session.delete(user)
    db.session.commit()

# Test for å opprette og hente en bruker fra databasen
def test_create_get_user(app, create_user):
    user = User.get_by_id(User, create_user.id)
    assert user is not None, "Bruker ble ikke funnet i db."
    assert user.name == 'test_user', "Feil brukernavn"

def test_update_password(app, create_user):
    with app.app_context():
        user = create_user
        user.password_hash = 'new_hash'
        db.session.commit()

        updated_user = User.get_by_id(User, user.id)
        assert updated_user.password_hash == 'new_hash', "Passordet ble ikke oppdatert."

# Tester CRUD-operasjoner for medication (Create, Read, Update, Delete)
def medication_crud_operations(app):
    with app.app_context():
        # Lager medication-objekt
        medication = Medication(day='Monday')
        db.session.add(medication)
        db.session.commit()

        # Leser medication-objekt fra db
        medication_entry = Medication.get_by_id(Medication, medication.id)
        assert medication_entry is not None, "medication ble ikke lagt til i db."
        assert medication_entry.day == 'Monday', "Feil dag"
        assert medication_entry.dose_1 is None, "Feil tidspunkt"

        # Oppdaterer medication-objekt
        medication_entry.dose_1 = '12:00'
        db.session.commit()

        # Leser oppdatert medication-objekt fra db
        updated_medication = Medication.get_by_id(Medication, medication.id)
        assert updated_medication.dose_1 == '12:00', "Tidspunkt ble ikke oppdatert."

        # Sletter medication-objekt
        db.session.delete(updated_medication)
        db.session.commit()

        # Leser slettet medication-objekt fra db
        deleted_medication = Medication.get_by_id(Medication, medication.id)
        assert deleted_medication is None, "medication ble ikke slettet."
        
# Test for AutoDoorLock statusendring
def test_autodoorlock_status(app):
    with app.app_context():
        # Lager AutoDoorLock-objekt
        autodoorlock = AutoDoorLock(time="10:00", status=False)
        db.session.add(autodoorlock)
        db.session.commit()
        
        # Leser AutoDoorLock-objekt fra db
        doorlock_entry = AutoDoorLock.get_by_id(AutoDoorLock, autodoorlock.id)
        assert doorlock_entry is not None, "AutoDoorLock ble ikke lagt til i db."
        assert doorlock_entry.status is False, "Dørstatus er feil"

        # Endrer status på AutoDoorLock-objekt til låst
        doorlock_entry.status = True
        db.session.commit()
        
        # Leser oppdatert AutoDoorLock-objekt fra db
        updated_doorlock = AutoDoorLock.get_by_id(AutoDoorLock, autodoorlock.id)
        assert updated_doorlock.status is True, "Dørstatus ble ikke oppdatert til låst"
