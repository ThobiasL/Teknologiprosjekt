# services/headunit_logic.py

from services.database_operations import DatabaseOperations

class HeadunitLogic:
    def __init__(self):
        self.db_ops = DatabaseOperations()

    def readVariableStatusFromDatabase(self):
        return self.db_ops.get_auto_door_lock_status()

    def sendAutoDoorLockTimeToDatabase(self, status):
        self.db_ops.set_auto_door_lock_status(status)

    def readMedicationDosesFromDatabase(self, day):
        return self.db_ops.get_medication_doses(day)

    def sendMedicationDosesStatusToDatabase(self, medication_id, dose_id):
        self.db_ops.set_medication_dose_status(medication_id, dose_id)

    def readTasksFromDatabase(self):
        return self.db_ops.get_all_tasks()

    def taskDone(self, name, time):
        self.db_ops.mark_task_done(name, time)
