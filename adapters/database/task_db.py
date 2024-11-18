from application.database import db
from adapters.database.base import Base

# Task-adapter for databasen
class Task(Base):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=True)
    scheduled = db.Column(db.Boolean, nullable=False, default=False)