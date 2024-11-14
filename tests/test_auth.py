import pytest
from flask import session
from application.database import db
from werkzeug.security import generate_password_hash
from adapters.database.user_db import User

# Test for suksessfull innlogging med riktig passord
def test_login_success(client, app, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "User 'test_user' was not found in the database."
        
    response = client.post('/login', data={'id': user.id, 'password': 'password1'})
    assert response.status_code == 302
    assert '/home' in response.location
    with client.session_transaction() as session:
        assert 'username' in session

# Test for feilet innlogging med feil passord
def test_login_fail(client, app, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "User 'test_user' was not found in the database."
        
    response = client.post('/login', data={'id': user.id, 'password': 'wrong_password'})
    assert response.status_code == 200
    assert b'Feil passord' in response.data
    with client.session_transaction() as session:
        assert 'username' not in session

# Test for tilgang til beskyttet side når bruker er innlogget
def test_access_protected_page_with_login(client, app, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "User 'test_user' was not found in the database."
        
    client.post('/login', data={'id': user.id, 'password': 'password1'})
    response = client.get('/home')
    assert response.status_code == 200

# Test for tilgang til beskyttet side uten innlogging
def test_access_protected_page_without_login(client):
    response = client.get('/home')
    assert response.status_code == 302
    assert '/login' in response.location
    with client.session_transaction() as session:
        assert 'username' not in session

# Test for å sikre at utlogging fungerer
def test_logout(client, app, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "User 'test_user' was not found in the database."
        
    client.post('/login', data={'id': user.id, 'password': 'password1'})
    response = client.get('/logout')
    assert response.status_code == 302
    assert '/login' in response.location
    with client.session_transaction() as session:
        assert 'username' not in session

# Test for å sikre at passord kan endres
def test_register_new_password(client, app, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "User 'test_user' was not found in the database."
        
    response = client.post('/register', data={'id': user.id, 'password': 'new_password'})
    assert response.status_code == 302
    assert '/register' in response.location
    response = client.post('/login', data={'id': user.id, 'password': 'new_password'})
    assert response.status_code == 302
    assert '/home' in response.location
    with client.session_transaction() as session:
        assert 'username' in session

# Test for innlogging uten data
def test_login_without_data(client):
    response = client.post('/login', data={})
    assert response.status_code == 200
    assert b'Feil passord' in response.data
    with client.session_transaction() as session:
        assert 'username' not in session

# Test for å hindre uautorisert passordendring
def test_unauthorized_password_change(client, app, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "User 'test_user' was not found in the database."
        
    response = client.post('/register', data={'id': user.id, 'password': 'unauthorized_password'})
    assert response.status_code == 302
    assert '/login' in response.location
    with app.app_context():
        user = User.query.get(user.id)
        assert user.check_password('password1')

# Test for blokkering av passordendring med et for svakt passord
def test_register_with_weak_password(client, app, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "User 'test_user' was not found in the database."
        
    response = client.post('/register', data={'id': user.id, 'password': '123'})
    assert response.status_code == 200
    assert b'Svak passord' in response.data

# Test for å verifisere at passord er korrekt hashet
def test_password_hashing(client, app, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        assert user is not None, "User 'test_user' was not found in the database."
        assert user.password_hash != 'password1'

# Test for innlogging med manglende brukernavn
def test_login_missing_username(client):
    response = client.post('/login', data={'password': 'password1'})
    assert response.status_code == 200
    assert b'Brukernavn kreves' in response.data

# Test for innlogging med manglende passord
def test_login_missing_password(client):
    response = client.post('/login', data={'id': 1})
    assert response.status_code == 200
    assert b'Passord kreves' in response.data

# Test for flere samtidige innlogginger
def test_multiple_logins(client, app, init_data):
    with app.app_context():
        user = User.query.filter_by(name='test_user').first()
        user2 = User.query.filter_by(name='test_user2').first()
        assert user is not None and user2 is not None, "Both test users should exist in the database."
        
    response1 = client.post('/login', data={'id': user.id, 'password': 'password1'})
    assert response1.status_code == 302
    response2 = client.post('/login', data={'id': user2.id, 'password': 'password2'})
    assert response2.status_code == 302
    with client.session_transaction() as session:
        assert session['username'] == user2.name

# Test for innlogging med ugyldig brukernavn
def test_login_invalid_username(client):
    response = client.post('/login', data={'id': 999, 'password': 'password'})
    assert response.status_code == 200
    assert b'Ugyldig brukernavn' in response.data
    with client.session_transaction() as session:
        assert 'username' not in session
