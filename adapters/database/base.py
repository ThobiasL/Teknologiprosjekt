from application.database import db

class Base(db.Model):
    __abstract__ = True

    @staticmethod
    def get_by_id(model, id):
        with db.session() as session:
            return session.get(model, id)

    def get(self, attribute):
        if hasattr(self, attribute):
            return getattr(self, attribute)
        raise AttributeError('Ugyldig attributt')

    def set(self, attribute, value):
        if hasattr(self, attribute):
            setattr(self, attribute, value)
            self.save()
        else:
            raise AttributeError('Ugyldig attributt')

    def save(self):
        with db.session() as session:
            session.add(self)
            session.commit()
