# Enhets- og integrasjonstester for kjernefunksjonalitet

import unittest
from application.database import db
from core.utils import verify_password, hash_password, is_valid_time
from adapters.database.user_db import User

# Enhetstester

# Test for hashing og verifisering av passord
def test_hash_verify_password():
    hashed = hash_password("testpassword")
    assert verify_password(hashed, "testpassword") is True
    assert verify_password(hashed, "wrongpassword") is False

# Test for is_valid_time med diverse tidspunkter
def test_is_valid_time():
    assert is_valid_time("12:30") is True
    assert is_valid_time("25:00") is False
    assert is_valid_time("12:61") is False
    assert is_valid_time("abc") is False
    assert is_valid_time("") is False

# Test for get_by_id-metode med gyldig bruker-id
def test_get_by_id_valid(app):
    with app.app_context():
        user = User(name="test_user", password_hash="hash")
        db.session.add(user)
        db.session.commit()
        fetched_user = User.get_by_id(User, user.id)
        assert fetched_user.id == user.id

# Test for get_by_id-metode med ugyldig bruker-id
def test_get_by_id_invalid(app):
    with app.app_context():
        user = User.get_by_id(User, 999)
        assert user is None
