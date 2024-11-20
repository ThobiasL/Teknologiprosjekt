from sqlalchemy.orm import Session
from adapters.database.core.autodoorlock_core import AutoDoorLock
from adapters.database.core.medication_core import Medication
from adapters.database.core.task_core import Task

class Headunit:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def readVariableStatusFromDatabase(self):
        autodoorlock = self.db_session.query(AutoDoorLock).get(1)
        if autodoorlock:
            return autodoorlock.status
        return None

    def readAutoDoorLockTimeFromDatabase(self):
        autodoorlock = self.db_session.query(AutoDoorLock).get(1)
        if autodoorlock:
            return autodoorlock.time
        return None

    def sendAutoDoorLockTimeToDatabase(self, status: int):
        autodoorlock = self.db_session.query(AutoDoorLock).get(1)
        if autodoorlock:
            autodoorlock.status = bool(status)
            self.db_session.commit()

    def readMedicationDosesFromDatabase(self, day: str):
        medication = self.db_session.query(Medication).filter_by(day=day).first()
        if medication:
            doses = {
                f"dose_{i}": getattr(medication, f"dose_{i}") for i in range(1, 5)
            }
            doses.update({
                f"scheduled_{i}": getattr(medication, f"scheduled_{i}") for i in range(1, 5)
            })
            return doses
        return {}

    def sendMedicationDosesStatusToDatabase(self, medication_id: int, dose_id: int):
        medication = self.db_session.query(Medication).get(medication_id)
        if medication:
            setattr(medication, f'scheduled_{dose_id}', False)
            self.db_session.commit()

    def readTasksFromDatabase(self):
        all_tasks = self.db_session.query(Task).filter_by(scheduled=True).all()
        tasks = []
        for task in all_tasks:
            tasks.append({"name": task.name, "time": task.time})
        return tasks

    def taskDone(self, name: str, time: str):
        task = self.db_session.query(Task).filter_by(name=name, time=time).first()
        if task:
            task.scheduled = False
            self.db_session.commit()

    # Ekstra funksjoner for eventuelle Viste-statusoperasjoner
    def readVisteStatusFromDatabase(self):
        autodoorlock = self.db_session.query(AutoDoorLock).get(1)
        if autodoorlock:
            return autodoorlock.status
        return None

    def sendVisteStatusToDatabase(self, status: bool):
        autodoorlock = self.db_session.query(AutoDoorLock).get(1)
        if autodoorlock:
            autodoorlock.status = status
            self.db_session.commit()
