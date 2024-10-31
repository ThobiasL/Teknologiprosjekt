from app import create_app
from app.models.user import User
from app.models.autodoorlock import AutoDoorLock
from app.models.autopilldispenser import AutoPillDispenser
from app.adapters.database import db
import os
from werkzeug.security import generate_password_hash

# Funksjon for å initialisere databasen
def initialize_database():

    db_path = 'data/app_data.db' # Path til databasen

    # Sjekker om data-mappen eksisterer, og lager den hvis den ikke gjør det
    if not os.path.exists('data'):
        os.makedirs('data')

    # Sjekker om databasen eksisterer, og lager den hvis den ikke gjør det
    app = create_app()
    with app.app_context():
        if not os.path.exists(db_path):
            db.create_all()

        # Legger til brukere i databasen
        existing_users = User.query.all()
        if not existing_users:
            
            default_password_hash = generate_password_hash(os.urandom(24).hex()) # Lager et sikkert, hashet defaultpassord til før brukerene er satt opp, konverterer til hex for å sikre databasekompatibilitet

            user1 = User(name='bruker', password_hash=default_password_hash)
            user2 = User(name='pårørende', password_hash=default_password_hash)
            user3 = User(name='andre', password_hash=default_password_hash)

            db.session.add(user1)
            db.session.add(user2)
            db.session.add(user3)
            db.session.commit()
            print('Brukere lagt til i databasen med standardpassord')

        # Legger til autodoorlock i databasen
        existing_autodoorlock = AutoDoorLock.query.all()
        if not existing_autodoorlock:
            autodoorlock = AutoDoorLock(lock_time=None, lock_status=False)

            db.session.add(autodoorlock)
            db.session.commit()
            print('Autodoorlock lagt til i databasen')

        # Legger til autopilldispenser i databasen
        existing_autopilldispenser = AutoPillDispenser.query.all()
        if not existing_autopilldispenser:
            autopilldispenser_time = AutoPillDispenser(autopilldispenser_time=None)

            db.session.add(autopilldispenser_time)
            db.session.commit()
            print('Autopilldispenser lagt til i databasen')

# Kjører funksjonen for å initialisere databasen
if __name__ == '__main__':
    initialize_database()