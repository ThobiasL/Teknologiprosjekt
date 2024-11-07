from application import db

class AutoDoorLock(db.Model):
    __tablename__ = 'autodoorlock'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, nullable=False, default=False)
    time = db.Column(db.String, nullable=True, default=None)

    def set_status(self, status):
        self.status = status
        db.session.commit()

    def set_time(self, time):
        self.time = time
        db.session.commit()
    
    
