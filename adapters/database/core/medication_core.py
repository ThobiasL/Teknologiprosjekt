# Databasemodell for Medication til kjernesiden av databasen.

from sqlalchemy import Column, Integer, String, Boolean
from adapters.database.core.base_core import Base, BaseMixin

class Medication(Base, BaseMixin):
    __tablename__ = 'medication'
    id = Column(Integer, primary_key=True)
    day = Column(String, nullable=False)
    dose_1 = Column(String, nullable=True, default=None)
    dose_2 = Column(String, nullable=True, default=None)
    dose_3 = Column(String, nullable=True, default=None)
    dose_4 = Column(String, nullable=True, default=None)
    scheduled_1 = Column(Boolean, nullable=False, default=False)
    scheduled_2 = Column(Boolean, nullable=False, default=False)
    scheduled_3 = Column(Boolean, nullable=False, default=False)
    scheduled_4 = Column(Boolean, nullable=False, default=False)