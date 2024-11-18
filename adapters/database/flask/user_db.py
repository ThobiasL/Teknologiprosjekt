from sqlalchemy import Column, Integer, String, Boolean
from adapters.database.base_flask import Base, BaseMixin
from core.utils import hash_password, verify_password

# Brukeradapter for databasen
class User(Base, BaseMixin):
    __tablename__ = 'users' # Tabellnavn i databasen

    # Kolonner i tabellen
    id = Column(Integer, primary_key=True) # Primærnøkkel
    name = Column(String(20), unique=True, nullable=False) # Brukernavn
    password_hash = Column(String(128), nullable=False) # Passord

    # Setter passordet til brukeren, hashet
    def set_password(self, password):
        self.password_hash = hash_password(password)

    # Sjekker passordet til brukeren
    def check_password(self, password):
        return verify_password(self.password_hash, password)