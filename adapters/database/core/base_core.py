# Basemodell med metoder for alle modeller på kjernesiden av databasen.

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Hjelpeklasse for generiske metoder, inneholder funksjon for å hente objekt fra databasen basert på id.
# Getter og setter, samt save-metode for å lagre endringer til databasen.
class BaseMixin:
    
    @classmethod
    def get_by_id(cls, session, id):
        return session.query(cls).get(id)

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
