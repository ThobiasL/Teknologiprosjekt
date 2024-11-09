from application import db
from werkzeug.security import generate_password_hash, check_password_hash
from core.models.base_model import BaseModel

# Brukermodell for databasen
class User(BaseModel):
    __tablename__ = 'users' # Tabellnavn i databasen

    # Kolonner i tabellen
    id = db.Column(db.Integer, primary_key=True) # Primærnøkkel
    name = db.Column(db.String(20), unique=True, nullable=False) # Brukernavn
    password_hash = db.Column(db.String(128), nullable=False) # Passord

    # Implementerer getter for navn og setter for passord
    def get(self, attribute):
        if attribute == 'name':
            return self.name
        else:
            raise ValueError('Ugyldig attributt')
        
    def set(self, attribute, value):
        if attribute == 'password':
            self.password_hash = generate_password_hash(value)
        else:
            raise ValueError('Ugyldig attributt')
        
        self.save()

    # Metode for å sjekke passord, sammenligner hashet passord med hashet passord i databasen
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    