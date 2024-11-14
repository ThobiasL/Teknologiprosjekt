import pytest
from flask import session
from application.database import db
from adapters.database.medication_db import Medication

# Test for å oppdatere en dosetid for medisinering når brukeren er logget inn
def test_update_medication_dose_with_login(client, app, login, init_data):
    login('test_user', 'password1')
    
    # Oppdater dosetid for dose 1 via `medication_dose`-ruten
    response = client.post('/medication/1/1', data={'set_time': 'true', 'time': '12:30'})
    assert response.status_code == 302  # Sjekker at vi blir omdirigert etter oppdatering

    # Verifiser at dosetiden er oppdatert
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)  # Henter første dose for dagen
        assert medication.get('dose_1') == '12:30'

def test_update_medication_dose_without_login(client, app, init_data):
    # Sjekk at brukeren ikke er logget inn
    with client.session_transaction() as session:
        assert 'username' not in session

    # Prøv å oppdatere dosetid uten innlogging
    response = client.post('/medication/1/1', data={'set_time': 'true', 'time': '12:30'})
    assert response.status_code == 302  # Sjekker at vi blir omdirigert
    assert '/login' in response.location  # Bekrefter at omdirigeringen er til login-siden

    # Verifiser at dosetiden ikke er oppdatert
    with app.app_context():
        medication = Medication.get_by_id(Medication, 1)  # Henter første dose for dagen
        assert medication.get('dose_1') != '12:30'
