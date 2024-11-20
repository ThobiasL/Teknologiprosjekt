import threading
import time
from sqlalchemy.orm import sessionmaker
from services.headunit import Headunit
import logging

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
        self.stop_event = threading.Event()  # Thread-safe stopp-mekanisme
        self.last_door_lock_status = None
        self.thread = threading.Thread(target=self.run, daemon=True)
        logging.basicConfig(level=logging.INFO)

    def start(self):
        """Starter tråden for å overvåke databaseoppdateringer."""
        if not self.thread.is_alive():
            self.thread.start()
            logging.info("PeriodicDatabaseReader started.")

    def stop(self):
        """Stopper overvåkingstråden."""
        self.stop_event.set()  # Signaliser stopp
        self.thread.join()  # Vent på at tråden avsluttes
        logging.info("PeriodicDatabaseReader stopped.")

    def run(self):
        """Periodisk overvåking av databaseoppdateringer."""
        while not self.stop_event.is_set():
            try:
                self.check_door_lock_status()
            except Exception as e:
                logging.error(f"Error during database check: {e}")
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

            # Sammenlign med tidligere status
            if current_status != self.last_door_lock_status:
                logging.info(f"Door lock status changed to {current_status}.")
                if self.on_door_lock_update:
                    self.on_door_lock_update(current_status)
                self.last_door_lock_status = current_status

        except Exception as e:
            logging.error(f"Failed to check door lock status: {e}")

        finally:
            if session:
                session.close()
