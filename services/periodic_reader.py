import threading
import time
from sqlalchemy.orm import sessionmaker
from services.headunit import Headunit

class PeriodicDatabaseReader:
    def __init__(self, db_session_factory: sessionmaker, on_door_lock_update=None, interval: float = 0.5):
        """
        Initierer periodisk overvåking av databaseoppdateringer.
        
        :param db_session_factory: Factory-funksjon for å opprette nye database sessions.
        :param on_door_lock_update: Callback-funksjon for oppdatering av dørlåsstatus.
        :param interval: Hvor ofte databasen skal overvåkes (default 0.5 sekunder).
        """
        self.db_session_factory = db_session_factory
        self.on_door_lock_update = on_door_lock_update
        self.interval = interval
        self.keep_running = True
        self.last_door_lock_status = None
        self.thread = threading.Thread(target=self.run, daemon=True)

    def start(self):
        """Starter tråden for å overvåke databaseoppdateringer."""
        self.thread.start()

    def stop(self):
        """Stopper overvåkingstråden."""
        self.keep_running = False
        self.thread.join()

    def run(self):
        """Periodisk overvåking av databaseoppdateringer."""
        while self.keep_running:
            try:
                self.check_door_lock_status()
            except Exception:
                pass  # Ignorer unntak
            time.sleep(self.interval)

    def check_door_lock_status(self):
        """Overvåker dørlåsstatus i databasen med SQLAlchemy."""
        session = None
        try:
            # Opprett en ny session
            session = self.db_session_factory()

            # Bruk Headunit-klassen for å lese dørlåsstatus
            headunit = Headunit(session)
            current_status = headunit.readVariableStatusFromDatabase()

            if current_status != self.last_door_lock_status:
                if self.on_door_lock_update:
                    self.on_door_lock_update(current_status)
                self.last_door_lock_status = current_status

        finally:
            if session:
                session.close()
