import os
from werkzeug.security import generate_password_hash
from application import create_app
from application.database import db
from adapters.database.user import User
from adapters.database.autodoorlock import AutoDoorLock
from adapters.database.medication import Medication
from adapters.database.task import Task

# Funksjon for å initialisere databasen
def initialize_database():
    # Sjekker om mappen til databasen eksisterer, og oppretter den om den ikke gjør det
    data_dir = os.path.join(os.path.dirname(__file__), '../..', 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Laget data-mappen for databaselagring")

    # Sjekker om databasen eksisterer, og oppretter den om den ikke gjør det
    app = create_app()
    with app.app_context():
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        # Opprett tabeller hvis databasen ikke eksisterer
        if not os.path.exists(db_path):
            db.create_all()
            print("Databasen ble opprettet.")

        # Legger til brukere i databasen om ingen brukere finnes
        if not db.session.query(User).first():
            default_password_hash = generate_password_hash(os.urandom(24).hex())  # Standard hashet passord, skal ikke håndteres slik i produksjon
            users = [
                User(name='Primærbruker', password_hash=default_password_hash),
                User(name='Pårørende', password_hash=default_password_hash),
                User(name='Gjest', password_hash=default_password_hash),
                User(name='Admin', password_hash=default_password_hash)
            ]
            db.session.add_all(users)
            db.session.commit()
            print("Standard-brukere lagt til i databasen med hashet standardpassord.")

        # Legger til AutoDoorLock-instans hvis ingen finnes
        if not db.session.query(AutoDoorLock).first():
            autodoorlock = AutoDoorLock(time=None, status=False)
            db.session.add(autodoorlock)
            db.session.commit()
            print("Autodoorlock-instans lagt til i databasen.")

        # Legger til Medication-instans hvis ingen finnes
        if not db.session.query(Medication).first():
            time = Medication(time=None)
            db.session.add(time)
            db.session.commit()
            print("Medication-instans lagt til i databasen.")

        # Legger til Task-instanser hvis ingen finnes
        if not db.session.query(Task).first():
            tasks = [
                Task(name='Medisin', time=None, scheduled=False),
                Task(name='Mat', time=None, scheduled=False),
                Task(name='Luft', time=None, scheduled=False)
            ]
            db.session.add_all(tasks)
            db.session.commit()
            print("Standard-oppgaver til huskeliste lagt til i databasen.")        

        

# Kjører funksjonen for å initialisere databasen
if __name__ == '__main__':
    initialize_database()
