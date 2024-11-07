import os
from werkzeug.security import generate_password_hash
from app import create_app
from core.models.user import User
from core.models.autodoorlock import AutoDoorLock
from core.models.autopilldispenser import AutoPillDispenser
from adapters.database import db

# Funksjon for å initialisere databasen
def initialize_database():
    
    # Sjekker om mappen til databasen eksisterer, og oppretter den om den ikke gjør det
    basedir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(basedir, '..', 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Laget mappen {data_dir} for databaselagring.")

    # Sjekker om databasen eksisterer, og oppretter den om den ikke gjør det
    app = create_app()
    with app.app_context():
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        # Opprett tabeller hvis databasen ikke eksisterer
        if not os.path.exists(db_path):
            db.create_all()
            print("Databasen ble opprettet.")

        # Legger til brukere i databasen om ingen brukere finnes
        if not User.query.first():
            default_password_hash = generate_password_hash(os.urandom(24).hex())  # Standard hashet passord
            users = [
                User(name='bruker', password_hash=default_password_hash),
                User(name='pårørende', password_hash=default_password_hash),
                User(name='andre', password_hash=default_password_hash)
            ]
            db.session.add_all(users)
            db.session.commit()
            print("Standard brukere lagt til i databasen med hashet standardpassord.")

        # Legger til AutoDoorLock-instans hvis ingen finnes
        if not AutoDoorLock.query.first():
            autodoorlock = AutoDoorLock(time=None, status=False)
            db.session.add(autodoorlock)
            db.session.commit()
            print("Autodoorlock-instans lagt til i databasen.")

        # Legger til AutoPillDispenser-instans hvis ingen finnes
        if not AutoPillDispenser.query.first():
            autopilldispenser_time = AutoPillDispenser(autopilldispenser_time=None)
            db.session.add(autopilldispenser_time)
            db.session.commit()
            print("Autopilldispenser-instans lagt til i databasen.")

# Kjører funksjonen for å initialisere databasen
if __name__ == '__main__':
    initialize_database()
