from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # Ren SQLAlchemy Base

# Hjelpeklasse for generiske metoder
class BaseMixin:
    @staticmethod
    def get_by_id(session, model, id):
        return session.query(model).get(id)

    def get(self, attribute):
        if hasattr(self, attribute):
            return getattr(self, attribute)
        raise AttributeError('Ugyldig attributt')

    def set(self, session, attribute, value):
        if hasattr(self, attribute):
            setattr(self, attribute, value)
            self.save(session)
        else:
            raise AttributeError('Ugyldig attributt')

    def save(self, session):
        session.add(self)
        session.commit()
