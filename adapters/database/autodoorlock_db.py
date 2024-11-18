from adapters.database.base import Base

# Autodoorlock-adapter for databasen
class AutoDoorLock(Base):
    __tablename__ = 'autodoorlock'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, nullable=False, default=False)
    time = db.Column(db.String, nullable=True, default=None)
    
    
