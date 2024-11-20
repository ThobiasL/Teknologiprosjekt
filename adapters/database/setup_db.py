import os
from adapters.database.core.database_core import init_db, SessionLocal  # Ren SQLAlchemy-konfigurasjon
from core.utils import hash_password
from adapters.database.core.user_core import User
from adapters.database.core.autodoorlock_core import AutoDoorLock
from adapters.database.core.medication_core import Medication
from adapters.database.core.task_core import Task    

# Initialiserer databasen med standardverdier, brukere får et felles, tilfeldig, hashet passord
# Database-filen blir lagret i data/database.db, og mappen blir laget dersom den ikke eksisterer
def initialize_database():
    # Sjekk og opprett databasekatalogen
    data_dir = os.path.join(os.path.dirname(__file__), '../..', 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Laget data-mappen for databaselagring")

    init_db()
    session = SessionLocal()

    try:
        if not session.query(User).first():
            default_password_hash = hash_password(os.urandom(24).hex())
            users = [
                User(name='Primærbruker', password_hash=default_password_hash),
                User(name='Pårørende', password_hash=default_password_hash),
                User(name='Gjest', password_hash=default_password_hash),
                User(name='Admin', password_hash=default_password_hash)
            ]
            session.add_all(users)
            session.commit()
            print("Standard-brukere lagt til i databasen.")

        # Legg til AutoDoorLock-instans
        if not session.query(AutoDoorLock).first():
            autodoorlock = AutoDoorLock(time=None, status=False)
            session.add(autodoorlock)
            session.commit()
            print("Autodoorlock-instans lagt til i databasen.")

        # Legg til Medication-instanser
        if not session.query(Medication).first():
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            medication = [Medication(day=day, dose_1=None, dose_2=None, dose_3=None, dose_4=None) for day in days]
            session.add_all(medication)
            session.commit()
            print("Medication-instanser lagt til i databasen.")

        # Legg til Task-instanser
        if not session.query(Task).first():
            tasks = [Task(name='Medisin', time=None), Task(name='Mat', time=None), Task(name='Luft', time=None)]
            session.add_all(tasks)
            session.commit()
            print("Standard-oppgaver lagt til i databasen.")
    finally:
        session.close()

if __name__ == '__main__':
    initialize_database()
