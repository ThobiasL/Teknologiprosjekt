from app import db

class AutoDoorLock(db.Model):
    __tablename__ = 'autodoorlock'
    id = db.Column(db.Integer, primary_key=True)
    lock_status = db.Column(db.Boolean, nullable=False, default=False)
    lock_time = db.Column(db.DateTime, nullable=True)

    def setLockStatus(self, status):
        self.lock_status = status

    def getLockStatus(self):
        return self.lock_status
    
    def setLockTime(self, time):
        self.lock_time = time

    def getLockTime(self):
        return self.lock_time
