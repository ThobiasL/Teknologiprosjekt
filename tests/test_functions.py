# Integrasjonstester for funksjoner i applikasjonen
# Begrenser mengden tester til moduler med unik funksjonalitet

import pytest
from flask import session
from adapters.database.flask.database_flask import db
from adapters.database.medication_flask import Medication
from adapters.database.autodoorlock_flask import AutoDoorLock

def test_lock_door_with_login(client, app, login, init_data):
    login('test_user', 'password')
    with app.app_context():
        autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        assert autodoorlock.status is False, "Døren er allerede låst."

    response = client.post('/lock_door')
    assert response.status_code == 302, "Døren ble ikke låst."

    with app.app_context():
        locked_autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        assert locked_autodoorlock.status is True, "Døren ble ikke låst."

def test_unlock_door_with_login(client, app, login, init_data):
    login('test_user', 'password')
    with app.app_context():
        autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        autodoorlock.status = True
        db.session.commit()
        assert autodoorlock.status is True, "Døren er allerede låst opp."

    response = client.post('/unlock_door')
    assert response.status_code == 302, "Døren ble ikke låst opp."

    with app.app_context():
        unlocked_autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        assert unlocked_autodoorlock.status is False, "Døren ble ikke låsto pp."

# Test for å låse døren uten innlogging
def test_lock_door_without_login(client, app, init_data):
    with client.session_transaction() as session:
        assert 'username' not in session

    response = client.post('/lock_door')
    assert response.status_code == 302
    assert '/login' in response.location

    with app.app_context():
        locked_autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        assert locked_autodoorlock.status is False

# Test for å låse opp døren uten innlogging
def test_unlock_door_without_login(client, app, init_data):
    with client.session_transaction() as session:
        assert 'username' not in session

    with app.app_context():
        autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        autodoorlock.status = True
        db.session.commit()
        assert autodoorlock.status is True

    response = client.post('/unlock_door')
    assert response.status_code == 302

    with app.app_context():
        unlocked_autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        assert unlocked_autodoorlock.status is True

# Test for å sette dosetid og aktivere med innlogging
def test_update_medication_dose_with_login(client, app, login, init_data):
    login('test_user', 'password')
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.dose_1 is None, "Dosetid er allerede satt."
    response = client.post('/medication/1/1', data={'set_time': 'true', 'time': '12:30'})
    assert response.status_code == 302, "Oppdatering ble ikke fullført."
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.dose_1 == '12:30', "Dosetid ble ikke oppdatert."
        assert medication.scheduled_1 is True, "Dosen ble ikke aktivert."

# Test for å sette dosetid og aktivere uten innlogging
def test_update_medication_dose_without_login(client, app, login, init_data):
    with client.session_transaction() as session:
        assert 'user_id' not in session, "Bruker er allerede logget inn."
    
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.dose_1 is None, "Dosetid er allerede satt."
    response = client.post('/medication/1/1', data={'set_time': 'true', 'time': '12:30'})
    assert response.status_code == 302, "Oppdatering ble ikke fullført."
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.dose_1 != '12:30', "Dosetid ble oppdatert."
        assert medication.scheduled_1 is not True, "Dosen ble aktivert."

# Test for å sette dosetid med ugyldig tid
def test_update_medication_dose_invalid_time(client, app, login, init_data):
    login('test_user', 'password')
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.dose_1 is None, "Dosetid er allerede satt."
    response = client.post('/medication/1/1', data={'set_time': 'true', 'time': '25:00'})
    assert response.status_code == 302, "Oppdatering ble fullført."
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.dose_1 is None, "Dosetid ble oppdatert."

# Test for å sette dosetid med ugyldig tid
def test_update_medication_dose_invalid_time2(client, app, login, init_data):
    login('test_user', 'password')
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.dose_1 is None, "Dosetid er allerede satt."
    response = client.post('/medication/1/1', data={'set_time': 'true', 'time': '12:61'})
    assert response.status_code == 302, "Oppdatering ble fullført."
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.dose_1 is None, "Dosetid ble oppdatert."

# Test for å sette dosetid med ugyldig tid
def test_update_medication_dose_empty_time(client, app, login, init_data):
    login('test_user', 'password')
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.dose_1 is None, "Dosetid er allerede satt."
    response = client.post('/medication/1/1', data={'set_time': 'true', 'time': ''})
    assert response.status_code == 302, "Oppdatering ble fullført."
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.dose_1 is None, "Dosetid ble oppdatert."

# Test for å sette dosetid med ugyldig tid
def test_update_medication_dose_partial_time(client, app, login, init_data):
    login('test_user', 'password')
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.dose_1 is None, "Dosetid er allerede satt."
    response = client.post('/medication/1/1', data={'set_time': 'true', 'time': '12'})
    assert response.status_code == 302, "Oppdatering ble fullført."
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.dose_1 is None, "Dosetid ble oppdatert."

# Test for å sette dosetid med ugyldig id
def test_update_medication_dose_invalid_id(client, app, login, init_data):
    login('test_user', 'password')
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.dose_1 is None, "Dosetid er allerede satt."
    response = client.post('/medication/1/2', data={'set_time': 'true', 'time': '12:30'})
    assert response.status_code == 302, "Oppdatering ble fullført."
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.dose_1 is None, "Dosetid ble oppdatert."

# Test for å aktivere dosetid med innlogging
def test_activate_medication_dose_with_login(client, app, login, init_data):
    login('test_user', 'password')
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.scheduled_1 is False, "Dosen er allerede aktivert."
    response = client.post('/medication/1/1', data={'toggle_schedule': 'true'})
    assert response.status_code == 302, "Oppdatering ble ikke fullført."
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.scheduled_1 is True, "Dosen ble ikke aktivert."

# Test for å aktivere dosetid uten innlogging
def test_activate_medication_dose_without_login(client, app, login, init_data):
    with client.session_transaction() as session:
        assert 'user_id' not in session, "Bruker er allerede logget inn."
    
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.scheduled_1 is False, "Dosen er allerede aktivert."
    response = client.post('/medication/1/1', data={'toggle_schedule': 'true'})
    assert response.status_code == 302, "Oppdatering ble ikke fullført."
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.scheduled_1 is not True, "Dosen ble aktivert."

# Test for å aktivere dosetid med ugyldig id
def test_activate_medication_dose_invalid_id(client, app, login, init_data):
    login('test_user', 'password')
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.scheduled_1 is False, "Dosen er allerede aktivert."
    response = client.post('/medication/1/2', data={'toggle_schedule': 'true'})
    assert response.status_code == 302, "Oppdatering ble fullført."
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.scheduled_1 is False, "Dosen ble aktivert."

# Test for å deaktivere dosetid med innlogging
def test_deactivate_medication_dose_with_login(client, app, login, init_data):
    login('test_user', 'password')
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        medication.set('scheduled_1', True)
        assert medication.scheduled_1 is True, "Dosen er allerede deaktivert."
    response = client.post('/medication/1/1', data={'toggle_schedule': 'true'})
    assert response.status_code == 302, "Oppdatering ble ikke fullført."
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)
        assert medication.scheduled_1 is False, "Dosen ble ikke deaktivert."