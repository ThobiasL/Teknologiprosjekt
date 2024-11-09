'''

import pytest
from flask import session
from adapters.database import db
from core.models.autodoorlock import AutoDoorLock

@pytest.fixture
def init_data(app):
    """Oppretter testdata i databasen"""
    with app.app_context():
        # Slett eventuelle eksisterende data
        db.session.query(AutoDoorLock).delete()

        # Legg til en ny AutoDoorLock-oppføring
        autodoorlock = AutoDoorLock(time=None, status=False)
        db.session.add(autodoorlock)
        db.session.commit()
        return autodoorlock.id

# Test for å oppdatere låsetiden
def test_update_lock_time(client, app, init_data):
    with app.app_context():
        # Send en POST-forespørsel for å sette låsetiden til '15:30'
        response = client.post('/update_lock_time', data={'time': '15:30'})
        assert response.status_code == 302  # Sjekker at vi blir omdirigert etter oppdatering

        # Sjekker at låsetiden i databasen er oppdatert
        updated_autodoorlock = db.session.get(AutoDoorLock, init_data)
        assert updated_autodoorlock.time == '15:30'

# Test for å låse døren
def test_lock_door(client, app, init_data):
    with app.app_context():
        # Send en POST-forespørsel for å låse døren
        response = client.post('/lock_door')
        assert response.status_code == 302  # Sjekker at vi blir omdirigert etter å ha låst døren

        # Sjekker at døren er satt til låst status i databasen
        locked_autodoorlock = db.session.get(AutoDoorLock, init_data)
        assert locked_autodoorlock.status is True

# Test for å låse opp døren
def test_unlock_door(client, app, init_data):
    with app.app_context():
        # Send en POST-forespørsel for å låse opp døren
        response = client.post('/unlock_door')
        assert response.status_code == 302  # Sjekker at vi blir omdirigert etter å ha låst opp døren

        # Sjekker at døren er satt til ulåst status i databasen
        unlocked_autodoorlock = db.session.get(AutoDoorLock, init_data)
        assert unlocked_autodoorlock.status is False
'''