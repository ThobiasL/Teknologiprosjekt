import pytest
from flask import session
from adapters.database import db
from core.models.user import User

# Test for å sjekke at innlogging fungerer med riktig passord
def test_login_success(client, init_data):
    user_id = init_data[0] # Henter ID til testbruker 1

    response = client.post('/login', data={'id': user_id, 'password': 'password1'}) # Sender POST-request til /login med riktig passord
    assert response.status_code == 302 # Sjekker at statuskoden er 302, som betyr at brukeren er videresendt
    assert '/home' in response.location # Sjekker at brukeren er videresendt til /home

    # Sjekker at brukeren er i session
    with client.session_transaction() as session:
        assert 'username' in session

# Test for å sjekke at innlogging feiler med feil passord
def test_login_fail(client, init_data):
    user_id = init_data[0] # Henter ID til testbruker 1

    response = client.post('/login', data={'id': user_id, 'password': 'wrong_password'})
    assert response.status_code == 200
    assert b'Feil passord' in response.data # Sjekker at feilmelding vises på siden

    # Sjekker at brukeren ikke er logget inn i session
    with client.session_transaction() as session:
        assert 'username' not in session

# Test for å sjekke at tilgang til beskyttet side med innlogging fungerer
def test_access_protected_page_with_login(client, init_data):
    user_id = init_data[0] # Henter ID til testbruker 1

    response = client.post('/login', data={'id': user_id, 'password': 'password1'}) # Logger inn bruker 1
    assert response.status_code == 302 # Sjekker at statuskoden er 302, som betyr at brukeren er videresendt
    assert '/home' in response.location # Sjekker at brukeren er videresendt til /home

    with client.session_transaction() as session:
        assert 'username' in session # Sjekker at brukeren er logget inn i session

    response = client.get('/home') # Sender GET-request til /home
    assert response.status_code == 200 # Sjekker at statuskoden er 200, som betyr at siden er lastet

# Test for å sjekke at tilgang til beskyttet side uten innlogging feiler
def test_access_protected_page_without_login(client):
    response = client.get('/home') # Sender GET-request til /home

    with client.session_transaction() as session:
        assert 'username' not in session

    assert response.status_code == 302 # Sjekker at statuskoden er 302, som betyr at brukeren er videresendt
    assert '/login' in response.location # Sjekker at brukeren er videresendt til /login

# Test for å sjekke at utlogging fungerer
def test_logout(client, init_data):
    user_id = init_data[0] # Henter ID til testbruker 1

    response = client.post('/login', data={'id': user_id, 'password': 'password1'}) # Logger inn bruker 1
    
    assert response.status_code == 302 # Sjekker at statuskoden er 302, som betyr at brukeren er videresendt
    assert '/home' in response.location # Sjekker at brukeren er videresendt til /home

    with client.session_transaction() as session:
        assert 'username' in session # Sjekker at brukeren er logget inn i session

    response = client.get('/logout') # Sender GET-request til /logout

    assert response.status_code == 302 # Sjekker at statuskoden er 302, som betyr at brukeren er videresendt
    assert '/login' in response.location # Sjekker at brukeren er videresendt til /login

    # Sjekker at brukeren ikke er logget inn i session
    with client.session_transaction() as session:
        assert 'username' not in session

# Test for å sjekke at passord kan endres
def test_register_new_password(client, init_data):

    user_id = init_data[0] # Henter ID til testbruker 1

    with client.application.app_context():
        response = client.post('/register', data={'id': user_id, 'password': 'new_password'}) # Sender POST-request til /register med nytt passord
        assert response.status_code == 302 # Sjekker at statuskoden er 302, som betyr at brukeren er videresendt
        assert '/register' in response.location # Sjekker at brukeren er videresendt til /register

        response = client.post('/login', data={'id': user_id, 'password': 'new_password'})
        assert response.status_code == 302
        assert '/home' in response.location

