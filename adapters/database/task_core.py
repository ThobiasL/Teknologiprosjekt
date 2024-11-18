from sqlalchemy import Column, Integer, String, Boolean
from adapters.database.base_core import Base, BaseMixin

# Task-adapter for databasen
class Task(Base, BaseMixin):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    time = Column(String, nullable=True)
    scheduled = Column(Boolean, nullable=False, default=False)