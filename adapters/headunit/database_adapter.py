from ports.database_port import DatabasePort
from adapters.database.core.database_core import SessionLocal
from services.headunit import Headunit

class DatabaseAdapter(DatabasePort):
    def __init__(self):
        self.session = SessionLocal()
        self.db = Headunit(self.session)

    # Returnerer fabrikkfunksjonen for å opprette nye sessions.
    def get_session_factory(self):
        """Returnerer fabrikkfunksjonen for å opprette nye sessions."""
        return SessionLocal

    # Leser status for variabel fra databasen.
    def send_auto_door_lock_time(self, status: int):
        self.db.sendAutoDoorLockTimeToDatabase(status)

    # Leser status for variabel fra databasen.
    def read_variable_status(self):
        return self.db.readVariableStatusFromDatabase()

    # Leser status for dørlås fra databasen.
    def read_auto_door_lock_time(self) -> str:
        doorlock_time = self.db.readAutoDoorLockTimeFromDatabase()
        return f"{doorlock_time}:00"

    # Leser status for dørlås fra databasen.
    def read_medication_doses(self, day: str) -> dict:
        return self.db.readMedicationDosesFromDatabase(day)

    # Leser status for dørlås fra databasen.
    def send_medication_dose_status(self, medication_id: int, dose_id: int):
        self.db.sendMedicationDosesStatusToDatabase(medication_id, dose_id)

    # Leser status for dørlås fra databasen.
    def read_tasks(self) -> list:
        return self.db.readTasksFromDatabase()

    # Leser status for dørlås fra databasen.
    def task_done(self, task_name: str, task_time: str):
        self.db.taskDone(task_name, task_time)

    #lokket session
    def close(self):
        self.session.close()