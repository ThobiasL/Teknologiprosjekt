# Integrasjonstester for innlogging, utlogging og autentisering

import pytest
from flask import session
from adapters.database.flask.database_flask import db
from adapters.database.flask.user_flask import User

# Tester at innlogging med riktig passord fungerer.
# Sjekker at brukeren finnes i databasen, at statuskoden er 302 (omdirigering),
# at brukeren videresendes til hjemmesiden, og at brukeren legges til i session.
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

# Tester at innlogging med feil passord ikke fungerer.
# Sjekker at brukeren finnes i databasen, at statuskoden er 200 (feilmelding vises),
# at en feilmelding vises på siden, og at brukeren ikke legges til i session.
def test_login_fail_wrong_password(client, app, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "Bruker {user.name} ble ikke funnet i db."
        
    response = client.post('/login', data={'id': user.id, 'password': 'wrong_password'})
    assert response.status_code == 200
    assert b'Feil passord' in response.data
    with client.session_transaction() as session:
        assert 'user_id' not in session

# Tester at innlogging med ugyldig brukernavn feiler.
# Sjekker at statuskoden er 200 (feilmelding vises), at en feilmelding om ukjent bruker vises,
# og at brukeren ikke legges til i session.
def test_login_invalid_username(client):
    response = client.post('/login', data={'id': 999, 'password': 'password'})
    assert response.status_code == 200
    assert b'Brukeren finnes ikke' in response.data
    with client.session_transaction() as session:
        assert 'user_id' not in session, "Bruker er innlogget."

# Tester at innlogging gir tilgang til en beskyttet side.
# Sjekker at brukeren finnes i databasen, og at statuskoden for tilgang til den
# beskyttede siden er 200 (vellykket).
def test_access_protected_page_with_login(client, app, login, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "Bruker ikke funnet i db."
        
    login(user.name, 'password')

    response = client.get('/home')
    assert response.status_code == 200, "Bruker ble ikke videresendt til hjemmesiden."

# Tester at brukere uten innlogging ikke har tilgang til en beskyttet side.
# Sjekker at brukeren ikke finnes i session, at statuskoden for tilgang er 302 (omdirigering),
# og at brukeren videresendes til innloggingssiden.
def test_access_protected_page_without_login(client):
    with client.session_transaction() as session:
        assert 'user_id' not in session, "Bruker er innlogget."
    response = client.get('/home')
    assert response.status_code == 302, "Bruker ble ikke videresendt."
    assert '/login' in response.location, "Bruker ble ikke videresendt til innlogging."

# Tester at utlogging fungerer korrekt.
# Sjekker at brukeren finnes i databasen, at utlogging gir statuskode 302 (omdirigering),
# at brukeren videresendes til innloggingssiden, og at brukeren fjernes fra session.
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

# Tester at brukeren kan oppdatere passordet sitt.
# Sjekker at brukeren finnes i databasen, at statuskoden er 302 (omdirigering),
# at brukeren videresendes til registreringssiden, og at innlogging fungerer med det nye passordet.
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

# Tester at brukeren ikke kan oppdatere passordet sitt til et tomt passord.
# Sjekker at brukeren finnes i databasen, at statuskoden er 200 (feilmelding vises),
# og at en passende feilmelding vises på siden.
def test_register_empty_password(client, app, login, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "Bruker {user.name} ble ikke funnet i db."
        
    response = client.post('/register', data={'id': user.id, 'password': ''})
    assert response.status_code == 200
    assert b'Bruker eller passord-feltet er tomt' in response.data, "Bruker endret passord til tomt felt."

# Tester at brukeren kan sette passord med spesialtegn.
# Sjekker at brukeren finnes i databasen, at statuskoden er 302 (omdirigering),
# og at innlogging fungerer med passordet med spesialtegn.
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

# Tester at brukeren kan sette passord med norske bokstaver.
# Sjekker at brukeren finnes i databasen, at statuskoden er 302 (omdirigering),
# og at innlogging fungerer med passordet med norske bokstaver.
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

# Tester at innlogging uten data feiler.
# Sjekker at statuskoden er 200 (feilmelding vises), og at en passende feilmelding vises på siden.
def test_login_without_data(client):
    response = client.post('/login', data={})
    assert response.status_code == 200 
    assert b'Fyll ut alle feltene' in response.data
    with client.session_transaction() as session:
        assert 'user_id' not in session, "Bruker er innlogget."

# Tester at passordene hashes korrekt.
# Sjekker at passordene ikke lagres i klartekst i databasen.
def test_password_hashing(client, app, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "Bruker ikke funnet i db"
        assert user.password_hash != 'password'

# Tester at innlogging med manglende brukernavn feiler.
# Sjekker at statuskoden er 200 (feilmelding vises), og at brukeren ikke logges inn.
def test_login_missing_username(client):
    response = client.post('/login', data={'password': 'password'})
    assert response.status_code == 200
    assert b'Fyll ut alle feltene' in response.data

# Tester at innlogging med manglende passord feiler.
# Sjekker at statuskoden er 200 (feilmelding vises), og at brukeren ikke logges inn.
def test_login_missing_password(client):
    response = client.post('/login', data={'id': 1})
    assert response.status_code == 200
    assert b'Fyll ut alle feltene' in response.data

# Tester at flere brukere kan logge inn sekvensielt.
# Sjekker at hver bruker legges til i session når de logger inn.
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

# Tester at flere feilede innlogginger ikke gir tilgang.
# Sjekker at brukeren ikke logges inn etter flere feilforsøk.
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

