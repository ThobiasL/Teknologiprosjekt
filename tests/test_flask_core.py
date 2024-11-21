# Enhets- og integrasjonstester for kjernefunksjonalitet

import pytest
import unittest
from adapters.database.flask.database_flask import db
from core.utils import verify_password, hash_password, is_valid_time
from adapters.database.flask.user_flask import User

# Enhetstester

# Tester at hashing og verifisering av passord fungerer.
# Sjekker at et korrekt passord validerer mot hash, og at et feil passord ikke validerer.
def test_hash_verify_password():
    hashed = hash_password("testpassword")
    assert verify_password(hashed, "testpassword") is True, "Passordet validerte ikke korrekt mot hash."
    assert verify_password(hashed, "wrongpassword") is False, "Feil passord validerte mot hash."

# Tester hashing og verifisering av tomme passordstrenger.
# Sjekker at tomme passord validerer korrekt og avvises med feil passord.
def test_hash_verify_password_empty():
    hashed = hash_password("")
    assert verify_password(hashed, "") is True, "Tom passordstreng validerte ikke korrekt."
    assert verify_password(hashed, "wrongpassword") is False, "Feil passord validerte mot tom hash."

# Tester hashing og verifisering av passord med spesialtegn.
# Sjekker at passord med spesialtegn validerer korrekt mot hash.
def test_hash_verify_password_special_chars():
    hashed = hash_password("testpassword!@#")
    assert verify_password(hashed, "testpassword!@#") is True, "Passord med spesialtegn validerte ikke korrekt."
    assert verify_password(hashed, "wrongpassword") is False, "Feil passord validerte mot hash med spesialtegn."

# Tester hashing og verifisering av passord med norske bokstaver.
# Sjekker at passord med æøå validerer korrekt mot hash.
def test_hash_verify_password_norwegian_chars():
    hashed = hash_password("testpasswordæøå")
    assert verify_password(hashed, "testpasswordæøå") is True, "Passord med norske bokstaver validerte ikke korrekt."
    assert verify_password(hashed, "wrongpassword") is False, "Feil passord validerte mot hash med norske bokstaver."

# Tester validering av tidsformater.
# Sjekker at gyldige tidsformater returnerer True og ugyldige tidsformater returnerer False.
def test_is_valid_time():
    assert is_valid_time("12:30") is True, "Gyldig tid ble ikke akseptert."
    assert is_valid_time("25:00") is False, "Ugyldig tid ble feilaktig akseptert."
    assert is_valid_time("12:61") is False, "Ugyldig tid med feil minutter ble feilaktig akseptert."
    assert is_valid_time("abc") is False, "Ugyldig tid med bokstaver ble feilaktig akseptert."
    assert is_valid_time("") is False, "Tom tid ble feilaktig akseptert."


# Tester get_by_id-metoden for å hente en bruker med gyldig ID.
# Sjekker at brukeren kan hentes korrekt fra databasen med riktig ID.
def test_get_by_id_valid(app):
    with app.app_context():
        user = User(name="test_user", password_hash="hash")
        db.session.add(user)
        db.session.commit()
        fetched_user = User.get_by_id(User, user.id)
        assert fetched_user.id == user.id, "Bruker med gyldig ID ble ikke hentet korrekt."

# Tester get_by_id-metoden for å hente en bruker med ugyldig ID.
# Sjekker at None returneres når ID ikke eksisterer i databasen.
def test_get_by_id_invalid(app):
    with app.app_context():
        user = User.get_by_id(User, 999)
        assert user is None, "Bruker med ugyldig ID returnerte noe annet enn None."
