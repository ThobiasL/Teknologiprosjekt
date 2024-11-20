# Databasemodell for AutoDoorLock til kjernesiden av databasen.

from sqlalchemy import Column, Integer, Boolean, String
from adapters.database.base_core import Base, BaseMixin

class AutoDoorLock(Base, BaseMixin):
    __tablename__ = 'autodoorlock'

    id = Column(Integer, primary_key=True)
    status = Column(Boolean, nullable=False, default=False)
    time = Column(String, nullable=True, default=None)
