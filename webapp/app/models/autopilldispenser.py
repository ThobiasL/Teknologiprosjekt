from app import db

class AutoPillDispenser(db.Model):
    __tablename__ = 'autopilldispenser'
    id = db.Column(db.Integer, primary_key=True)
    autopilldispenser_time = db.Column(db.DateTime, nullable=False)