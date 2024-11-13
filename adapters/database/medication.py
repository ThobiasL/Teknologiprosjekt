from application.database import db
from adapters.database.database_helper import DatabaseHelper

# Modell for Medication
class Medication(DatabaseHelper):
    __tablename__ = 'medication'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=True, default=None)
    scheduled = db.Column(db.Boolean, nullable=False, default=False)

    
    def get(self, attribute):
        if attribute == 'day':
            return self.day
        elif attribute == 'time':
            return self.time
        elif attribute == 'scheduled':
            return self.scheduled
        else:
            raise ValueError('Ugyldig attributt')
        
    def set(self, attribute, value):
        if attribute == 'day':
            self.day = value
        elif attribute == 'time':
            self.time = value
        elif attribute == 'scheduled':
            self.scheduled = value
        else:
            raise ValueError('Ugyldig attributt')
        
        self.save()

    