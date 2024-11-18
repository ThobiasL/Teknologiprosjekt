# Basisklasse for databasemodeller
class Base:
    __abstract__ = True # Gjør klassen abstrakt

    @staticmethod
    def get_db():
        from application.database import db
        return db


    # Metode for å hente en modell fra databasen basert på id
    @staticmethod
    def get_by_id(model, id):
        db = Base.get_db()
        return db.session.get(model, id)

    # Getter-metode
    def get(self, attribute):
        if hasattr(self, attribute):
            return getattr(self, attribute)
        raise AttributeError('Ugyldig attributt')

    # Setter-metode
    def set(self, attribute, value):
        if hasattr(self, attribute):
            setattr(self, attribute, value)
            self.save()
        else:
            raise AttributeError('Ugyldig attributt')

    # Metode for å lagre modellen i databasen
    def save(self):
        db = Base.get_db()
        db.session.add(self)
        db.session.commit()