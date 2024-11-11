import pytest
from flask import session
from application.database import db
from adapters.database.medication import Medication
from adapters.database.user import User

def login(client, app, user, password):
    with app.app_context():
        response = client.post('/login', data={'id': user.id, 'password': password})
        assert response.status_code == 302
        assert '/home' in response.location
        
    return response

# Test for å oppdatere låsetiden
def test_update_medication_time_with_login(client, app, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user1').first()  # Henter testbruker 1 fra databasen
    login(client, app, user, 'password1')

    response = client.post('/update_medication_time', data={'time': '12:30'})
    assert response.status_code == 302  # Sjekker at vi blir omdirigert etter oppdatering

    with app.app_context():
        updated_medication = db.session.query(Medication).first()
        assert updated_medication.time == '12:30'

# Test for å oppdatere låsetiden
def test_update_medication_time_without_login(client, app, init_data):
    with client.session_transaction() as session:
        assert 'username' not in session

    response = client.post('/update_medication_time', data={'time': '12:30'})
    assert response.status_code == 302  # Sjekker at vi blir omdirigert etter oppdatering
    assert '/login' in response.location

    with app.app_context():
        updated_medication = db.session.query(Medication).first()
        assert updated_medication.time != '12:30'

