from ports.database_port import DatabasePort
from application.database_core import SessionLocal
from services.headunit import Headunit

class DatabaseAdapter(DatabasePort):
    def __init__(self):
        self.session = SessionLocal()
        self.db = Headunit(self.session)
    
    def get_session_factory(self):
        """Returnerer fabrikkfunksjonen for å opprette nye sessions."""
        return SessionLocal

    def send_auto_door_lock_time(self, status: int):
        self.db.sendAutoDoorLockTimeToDatabase(status)

    def read_variable_status(self):
        return self.db.readVariableStatusFromDatabase()

    def read_auto_door_lock_time(self) -> str:
        doorlock_time = self.db.readAutoDoorLockTimeFromDatabase()
        return f"{doorlock_time}:00"

    def read_medication_doses(self, day: str) -> dict:
        return self.db.readMedicationDosesFromDatabase(day)

    def send_medication_dose_status(self, medication_id: int, dose_id: int):
        self.db.sendMedicationDosesStatusToDatabase(medication_id, dose_id)

    def read_tasks(self) -> list:
        return self.db.readTasksFromDatabase()

    def task_done(self, task_name: str, task_time: str):
        self.db.taskDone(task_name, task_time)

    def close(self):
        self.session.close()