# Integrasjonstester for visning av sider i applikasjonen

import pytest
from flask import session
from adapters.database.flask.database_flask import db
from adapters.database.flask.user_flask import User

# Test for root-rute med innlogging
def test_root_route_with_login(client, login, init_data):
    login('test_user', 'password')
    response = client.get('/')
    assert response.status_code == 302
    assert '/home' in response.location

# Test for root-rute uten innlogging
def test_root_route_without_login(client, init_data):
    with client.session_transaction() as session:
        assert 'user_id' not in session
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.location

# Test for AutoDoorLock-side
def test_autodoorlock_page(client, login, init_data):
    login('test_user', 'password')
    response = client.get('/lock_control')
    assert response.status_code == 200, "Siden ble ikke vist."
    page_content = response.data.decode('utf-8')
    assert 'Bekreft låsetid' in page_content, "Siden ble ikke vist riktig."

# Test for Medication-side
def test_medication_page(client, login, init_data):
    login('test_user', 'password')
    response = client.get('/medication')
    assert response.status_code == 200, "Siden ble ikke vist."
    assert b'Medisiner' in response.data, "Siden ble ikke vist riktig."

# Test for Tasks-side
def test_tasks_page(client, login, init_data):
    login('test_user', 'password')
    response = client.get('/tasks')
    assert response.status_code == 200, "Siden ble ikke vist."
    assert b'Huskeliste' in response.data, "Siden ble ikke vist riktig."

# Test for medication_day-siden
def test_medication_day(client, login, init_data):
    login('test_user', 'password')
    response = client.get('/medication/1')
    assert response.status_code == 200, "Medisin-siden ble ikke vist."
    assert b"Medisiner" in response.data, "Siden ble ikke vist riktig."

# Test for medication_day med ugyldig medisin-id
def test_medication_day_invalid_id(client, login, init_data):
    login('test_user', 'password')
    response = client.get('/medication/999')  # Antatt ugyldig ID
    assert response.status_code == 302, "Bruker ble ikke videresendt"
    assert "/medication" in response.location, "Bruker ble ikke videresendt til medisin-siden."

# Test for medication_dose 
def test_medication_dose_with_login(client, login, init_data):
    login('test_user', 'password')
    response = client.get('/medication/1/1')
    assert response.status_code == 200, "Dose-siden ble ikke vist."
    assert b"Dose 1" in response.data, "Siden ble ikke vist riktig."

# Test for medication_dose med ugyldig medisin-id
def test_medication_dose_invalid_id(client, login, init_data):
    login('test_user', 'password')
    response = client.get('/medication/1/999')  # Antatt ugyldig dose ID
    assert response.status_code == 302, "Bruker ble ikke videresendt"
    assert "/medication" in response.location, "Bruker ble ikke videresendt til medisin-siden."

