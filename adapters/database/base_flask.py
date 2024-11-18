from application.database import db
from abc import abstractmethod

# Hjelpeklasse for generiske metoder
class Base:
    __abstract__ = True

    @abstractmethod
    def get_by_id(model, id):
        return model.query.get(id)

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
