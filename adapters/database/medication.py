from application.database import db
from adapters.database.database_helper import DatabaseHelper

# Modell for Medication
class Medication(DatabaseHelper):
    __tablename__ = 'medication'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String, nullable=True, default=None)

    
    def get(self, attribute):
        if attribute == 'time':
            return self.time
        else:
            raise ValueError('Ugyldig attributt')
        
    def set(self, attribute, value):
        if attribute == 'time':
            self.time = value
        else:
            raise ValueError('Ugyldig attributt')
        
        self.save()

    