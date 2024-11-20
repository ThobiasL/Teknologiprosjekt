# Integrasjonstester for innlogging, utlogging og autentisering

import pytest
from flask import session
from adapters.database.flask.database_flask import db
from adapters.database.flask.user_flask import User

# Test for innlogging med riktig passord
def test_login_success(client, app, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "Bruker 'test_user' ble ikke funnet i db."
        
    response = client.post('/login', data={'id': user.id, 'password': 'password'})

    assert response.status_code == 302, "Bruker ble ikke videresendt."
    assert '/home' in response.location, "Bruker ble ikke videresendt til hjemmesiden."

    with client.session_transaction() as session:
        assert 'user_id' in session, "Bruker ble ikke lagt til i session. 1"
        assert session['user_id'] == user.id, "Bruker ble ikke lagt til i session. 2"

# Test for feilet innlogging med feil passord
def test_login_fail(client, app, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "Bruker {user.name} ble ikke funnet i db."
        
    response = client.post('/login', data={'id': user.id, 'password': 'wrong_password'})
    assert response.status_code == 200
    assert b'Feil passord' in response.data
    with client.session_transaction() as session:
        assert 'username' not in session

# Test for innlogging med ugyldig brukernavn
def test_login_invalid_username(client):
    response = client.post('/login', data={'id': 999, 'password': 'password'})
    assert response.status_code == 200
    assert b'Brukeren finnes ikke' in response.data
    with client.session_transaction() as session:
        assert 'username' not in session, "Bruker er innlogget."

# Test for tilgang til beskyttet side når bruker er innlogget
def test_access_protected_page_with_login(client, app, login, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "Bruker ikke funnet i db."
        
    login(user.name, 'password')

    response = client.get('/home')
    assert response.status_code == 200, "Bruker ble ikke videresendt til hjemmesiden."

# Test for tilgang til beskyttet side uten innlogging
def test_access_protected_page_without_login(client):
    with client.session_transaction() as session:
        assert 'user_id' not in session, "Bruker er innlogget."
    response = client.get('/home')
    assert response.status_code == 302, "Bruker ble ikke videresendt."
    assert '/login' in response.location, "Bruker ble ikke videresendt til innlogging."

# Test for å sikre at utlogging fungerer
def test_logout(client, app, login, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "Bruker {user.name} ble ikke funnet i db."
        
    login(user.name, 'password')
    response = client.get('/logout')
    assert response.status_code == 302, "Bruker ble ikke videresendt."
    assert '/login' in response.location, "Bruker ble ikke videresendt til innlogging."
    with client.session_transaction() as session:
        assert 'user_id' not in session, "Bruker er innlogget."

# Test for å sikre at passord kan endres
def test_register_new_password(client, app, login, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "Bruker {user.name} ble ikke funnet i db."
        
    response = client.post('/register', data={'id': user.id, 'password': 'new_password'})
    assert response.status_code == 302, "Bruker ble ikke videresendt."
    assert '/register' in response.location, "Bruker ble ikke videresendt til register-siden."

    login(user.name, 'new_password')

    with client.session_transaction() as session:
        assert 'user_id' in session, "Bruker ble ikke lagt til i session."

# Test for å sikre at passord ikke kan endres til tomt felt
def test_register_empty_password(client, app, login, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "Bruker {user.name} ble ikke funnet i db."
        
    response = client.post('/register', data={'id': user.id, 'password': ''})
    assert response.status_code == 200
    assert b'Bruker eller passord-feltet er tomt' in response.data, "Bruker endret passord til tomt felt."

# Test for å verifisere at passord med spesialtegn kan settes
def test_register_new_password_special_chars(client, app, login, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "Bruker {user.name} ble ikke funnet i db."
        
    response = client.post('/register', data={'id': user.id, 'password': 'new_password!@#'})
    assert response.status_code == 302, "Bruker ble ikke videresendt."
    assert '/register' in response.location, "Bruker ble ikke videresendt til register-siden."

    login(user.name, 'new_password!@#')

    with client.session_transaction() as session:
        assert 'user_id' in session, "Bruker ble ikke lagt til i session."

# Test for å verifisere at passord med norske bokstaver kan settes
def test_register_new_password_norwegian_chars(client, app, login, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "Bruker {user.name} ble ikke funnet i db."
        
    response = client.post('/register', data={'id': user.id, 'password': 'new_passwordæøå'})
    assert response.status_code == 302, "Bruker ble ikke videresendt."
    assert '/register' in response.location, "Bruker ble ikke videresendt til register-siden."

    login(user.name, 'new_passwordæøå')

    with client.session_transaction() as session:
        assert 'user_id' in session, "Bruker ble ikke lagt til i session."

# Test for innlogging uten data
def test_login_without_data(client):
    response = client.post('/login', data={})
    assert response.status_code == 200 
    assert b'Fyll ut alle feltene' in response.data
    with client.session_transaction() as session:
        assert 'user_id' not in session, "Bruker er innlogget."

# Test for å verifisere at passord er korrekt hashet
def test_password_hashing(client, app, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "Bruker ikke funnet i db"
        assert user.password_hash != 'password'

# Test for innlogging med manglende brukernavn
def test_login_missing_username(client):
    response = client.post('/login', data={'password': 'password'})
    assert response.status_code == 200
    assert b'Fyll ut alle feltene' in response.data

# Test for innlogging med manglende passord
def test_login_missing_password(client):
    response = client.post('/login', data={'id': 1})
    assert response.status_code == 200
    assert b'Fyll ut alle feltene' in response.data

# Test for flere samtidige innlogginger
def test_multiple_logins(client, app, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        user2 = User.query.filter_by(name='test_user2').first()
        assert user is not None and user2 is not None, "Begge brukere må eksistere i db."
        
    response1 = client.post('/login', data={'id': user.id, 'password': 'password'})
    assert response1.status_code == 302
    response2 = client.post('/login', data={'id': user2.id, 'password': 'password2'})
    assert response2.status_code == 302
    with client.session_transaction() as session:
        assert session['user_id'] == user2.id

# Test for flere feilede innlogginger
def test_multiple_failed_logins(client, app, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "Bruker 'test_user' ble ikke funnet i db."
    
    for _ in range(3):
        response = client.post('/login', data={'id': user.id, 'password': 'wrong_password'})
        assert response.status_code == 200
        assert b'Feil passord' in response.data

    with client.session_transaction() as session:
        assert 'user_id' not in session, "Bruker skal ikke være innlogget etter flere feilede forsøk."

