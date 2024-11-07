from application import db

class Medication(db.Model):
    __tablename__ = 'medication'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=True)

    def set_time(self, time):
        self.medication_time = time
    
    def get_time(self):
        return self.medication_time
    