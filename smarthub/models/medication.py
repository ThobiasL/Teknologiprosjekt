from application.database import db
from core.models.base_model import BaseModel

# Modell for Medication
class Medication(BaseModel):
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

    