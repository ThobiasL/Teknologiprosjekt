import pytest
from flask import session

def test_login_success(client):
    response = client.post('/login', data={'id': 1, 'password': 'password1'}) # Sender POST-request til /login med testbruker 1

    assert response.status_code == 302 # Sjekker at statuskoden er 302, som betyr at brukeren er videresendtr
    assert response.location.endswith('/home') # Sjekker at brukeren er videresendt til /home

    # sjekekr at brukeren er logget inn i session
    with client.session_transaction() as session:
        assert 'username' in session
        assert session['username'] == 'test_user1'

def test_login_fail(client):
    response = client.post('/login', data={'id': 1, 'password': 'wrong_password'}) # Sender POST-request til /login med feil passord

    assert response.status_code == 200 # Sjekker at statuskoden er 200, som betyr at siden er lastet på nytt
    assert b'Feil passord' in response.data # Sjekker at feilmelding vises på siden

    # Sjekker at brukeren ikke er logget inn i session
    with client.session_transaction() as session:
        assert 'username' not in session

def test_access_protected_page_with_login(client):
    client.post('/login', data={'id': 1, 'password': 'password1'}) # Logger inn bruker 1
    response = client.get('/home') # Sender GET-request til /home

    assert response.status_code == 302 # Sjekker at statuskoden er 302, som betyr at brukeren er videresendt
    assert '/home' in response.location # Sjekker at brukeren er videresendt til /home


def test_access_protected_page_without_login(client):
    response = client.get('/home') # Sender GET-request til /home

    assert response.status_code == 302 # Sjekker at statuskoden er 302, som betyr at brukeren er videresendt
    assert '/login' in response.location # Sjekker at brukeren er videresendt til /login