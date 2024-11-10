from application.database import db
from core.models.base_model import BaseModel

# Modell for AutoDoorLock
class AutoDoorLock(BaseModel):
    __tablename__ = 'autodoorlock'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, nullable=False, default=False)
    time = db.Column(db.String, nullable=True, default=None)

    # Implementer get og set metoder fra base_model for å lese eller endre tid og status

    def get(self, attribute):
        if attribute == 'time':
            return self.time
        elif attribute == 'status':
            return self.status
        else:
            raise ValueError('Ugyldig attributt')
    
    def set(self, attribute, value):
        if attribute == 'time':
            self.time = value
        elif attribute == 'status':
            self.status = value
        else:
            raise ValueError('Ugyldig attributt')
        
        self.save()
    
    
