from application.database import db
from adapters.database.base import Base

class AutoDoorLock(Base):
    __tablename__ = 'autodoorlock'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String, nullable=True)
    status = db.Column(db.Boolean, default=False)
