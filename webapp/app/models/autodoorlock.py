from app import db

class AutoDoorLock(db.Model):
    __tablename__ = 'autodoorlock'
    id = db.Column(db.Integer, primary_key=True)
    lock_status = db.Column(db.Boolean, nullable=False, default=False)
    lock_time = db.Column(db.DateTime, nullable=False)
