import pytest
from flask import session
from application.database import db
from adapters.database.autodoorlock import AutoDoorLock
from adapters.database.user import User



# Test for å oppdatere låsetiden
def test_update_lock_time_with_login(client, app, login, init_data):
    login('test_user1', 'password1')
    
    response = client.post('/update_lock_time', data={'time': '15:30'})
    assert response.status_code == 302  # Sjekker at vi blir omdirigert etter oppdatering

    with app.app_context():
        updated_autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        assert updated_autodoorlock.time == '15:30'

# Test for å låse døren
def test_lock_door_with_login(client, app, login, init_data):
    login('test_user1', 'password1')

    response = client.post('/lock_door')
    assert response.status_code == 302

    with app.app_context():
 
        locked_autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        assert locked_autodoorlock.status is True

def test_update_door_empty_time(client, app, login, init_data):
    login('test_user1', 'password1')

    response = client.post('/update_lock_time', data={'time': ''})
    assert response.status_code == 302  

    with app.app_context():
        updated_autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        assert updated_autodoorlock.time != ''

def test_update_door_invalid_time(client, app, login, init_data):
    login('test_user1', 'password1')

    response = client.post('/update_lock_time', data={'time': '25:00'})
    assert response.status_code == 302  # Sjekker at vi blir omdirigert etter oppdatering

    with app.app_context():
        updated_autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        assert updated_autodoorlock.time != '25:00'

def test_update_door_invalid_time2(client, app, login, init_data):
    login('test_user1', 'password1')

    response = client.post('/update_lock_time', data={'time': '12:60'})
    assert response.status_code == 302  # Sjekker at vi blir omdirigert etter oppdatering

    with app.app_context():
        updated_autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        assert updated_autodoorlock.time != '12:60'

# Test for å låse opp døren
def test_unlock_door_with_login(client, app, login, init_data):
    login('test_user1', 'password1')

    with app.app_context():
        autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        autodoorlock.status = True
        db.session.commit()
        assert autodoorlock.status is True
    
    # Send en POST-forespørsel for å låse opp døren
    response = client.post('/unlock_door')
    assert response.status_code == 302  # Sjekker at vi blir omdirigert etter å ha låst opp døren

    with app.app_context():
        # Sjekker at døren er satt til ulåst status i databasen
        unlocked_autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        assert unlocked_autodoorlock.status is False

# Test for å oppdatere låsetiden
def test_update_lock_time_without_login(client, app, init_data):
    with client.session_transaction() as session:
        assert 'username' not in session

    response = client.post('/update_lock_time', data={'time': '15:30'})
    assert response.status_code == 302  # Sjekker at vi blir omdirigert etter oppdatering
    assert '/login' in response.location

    with app.app_context():
        updated_autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        assert updated_autodoorlock.time != '15:30'

# Test for å låse døren
def test_lock_door_without_login(client, app, init_data):
    with client.session_transaction() as session:
        assert 'username' not in session

    # Send en POST-forespørsel for å låse døren
    response = client.post('/lock_door')
    assert response.status_code == 302  # Sjekker at vi blir omdirigert etter å ha låst døren
    assert '/login' in response.location

    with app.app_context():
        # Sjekker at døren er satt til låst status i databasen
        locked_autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        assert locked_autodoorlock.status is False

# Test for å låse opp døren
def test_unlock_door_without_login(client, app, init_data):
    with client.session_transaction() as session:
        assert 'username' not in session

    with app.app_context():
        autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        autodoorlock.status = True
        db.session.commit()
        assert autodoorlock.status is True

    # Send en POST-forespørsel for å låse opp døren
    response = client.post('/unlock_door')
    assert response.status_code == 302  # Sjekker at vi blir omdirigert etter å ha låst opp døren

    with app.app_context():
        # Sjekker at døren er satt til ulåst status i databasen
        unlocked_autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        assert unlocked_autodoorlock.status is True
