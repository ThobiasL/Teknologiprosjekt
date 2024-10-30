from app import create_app
from app.models.user import User
from app.adapters.database import db

def initialize_database():
    app = create_app()
    with app.app_context():
        db.create_all()

        existing_users = User.query.all()
        if not existing_users:
            user1 = User(username='bruker')
            user2 = User(username='pårørende')
            user3 = User(username='andre')

            db.session.add(user1)
            db.session.add(user2)
            db.session.add(user3)
            db.session.commit()
            print('Brukere lagt til i databasen')

if __name__ == '__main__':
    initialize_database()