from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Brukermodell for databasen
class User(db.Model):
    __tablename__ = 'users' # Tabellnavn i databasen

    # Kolonner i tabellen
    id = db.Column(db.Integer, primary_key=True) # Primærnøkkel
    username = db.Column(db.Integer, unique=True, nullable=False) # Brukernavn
    password_hash = db.Column(db.String(128), nullable=True)

    # Metode for å sette passord, hasher passordet før det lagres i databasen
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Metode for å sjekke passord, sammenligner hashet passord med hashet passord i databasen
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    