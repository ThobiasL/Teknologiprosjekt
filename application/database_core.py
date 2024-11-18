from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from adapters.database.base_flask import Base  # Base-klassen for modellene
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../data/database.db')

# Opprett SQLAlchemy-engine og session
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = scoped_session(sessionmaker(bind=engine))

# Funksjon for å opprette tabeller (brukes i standalone-kontekst)
def init_db():
    Base.metadata.create_all(bind=engine)
