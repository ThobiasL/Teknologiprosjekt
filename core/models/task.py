from application import db
from core.models.base_model import BaseModel

# Modell for Task
class Task(BaseModel):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=True)
    scheduled = db.Column(db.Boolean, nullable=False, default=False)

    # Implementer get-metode for å lese fra databasen
    def get(self, attribute):
        if attribute == 'name':
            return self.name
        elif attribute == 'time':
            return self.time
        elif attribute == 'scheduled':
            return self.scheduled
        else:
            raise ValueError('Ugyldig attributt')
    
    # Implementer set-metode for å endre i databasen
    def set(self, attribute, value):
        if attribute == 'time':
            self.time = value
        elif attribute == 'scheduled':
            self.scheduled = value
        else:
            raise ValueError('Ugyldig attributt')
        
        self.save()