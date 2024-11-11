from application.database import db

# Base-model for alle modeller
class DatabaseHelper(db.Model):
    __abstract__ = True # Gjør klassen abstrakt

    # Metode for å hente en modell fra databasen basert på id
    @staticmethod
    def get_by_id(model, id):
        return db.session.get(model, id)

    # Getter-metode
    def get(self, attribute):
        raise NotImplementedError

    # Setter-metode
    def set(self, attribute, value):
        raise NotImplementedError

    # Metode for å lagre modellen i databasen
    def save(self):
        db.session.add(self)
        db.session.commit()