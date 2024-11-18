from adapters.database.base import Base

# Medication-modell for databasen
class Medication(Base):
    __tablename__ = 'medication'

    db = Base.get_db()
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False)
    dose_1 = db.Column(db.String, nullable=True, default=None)
    dose_2 = db.Column(db.String, nullable=True, default=None)
    dose_3 = db.Column(db.String, nullable=True, default=None)
    dose_4 = db.Column(db.String, nullable=True, default=None)
    scheduled_1 = db.Column(db.Boolean, nullable=False, default=False)
    scheduled_2 = db.Column(db.Boolean, nullable=False, default=False)
    scheduled_3 = db.Column(db.Boolean, nullable=False, default=False)
    scheduled_4 = db.Column(db.Boolean, nullable=False, default=False)