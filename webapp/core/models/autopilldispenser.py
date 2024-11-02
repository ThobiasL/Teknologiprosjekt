from app import db

class AutoPillDispenser(db.Model):
    __tablename__ = 'autopilldispenser'
    id = db.Column(db.Integer, primary_key=True)
    autopilldispenser_time = db.Column(db.DateTime, nullable=True)

    def setAutoPillDispenserTime(self, time):
        self.autopilldispenser_time = time
    
    def getAutoPillDispenserTime(self):
        return self.autopilldispenser_time
    