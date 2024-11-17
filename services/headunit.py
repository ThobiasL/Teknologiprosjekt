# services/headunit.py
from services.database_operations import DatabaseOperations

class Headunit:
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



class Headunit:
    def __init__(self):
        pass

    def readVariableStatusFromDatabase(self):
        from adapters.database.autodoorlock_db import AutoDoorLock
        autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        status = autodoorlock.get('status')
        return status

    def readAutoDoorLockTimeFromDatabase(self):
        from adapters.database.autodoorlock_db import AutoDoorLock
        autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        time = autodoorlock.get('time')
        return time

    def sendAutoDoorLockTimeToDatabase(self, status):
        from adapters.database.autodoorlock_db import AutoDoorLock
        autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        if status == 1:
            autodoorlock.set('status', True)
        elif status == 0:
            autodoorlock.set('status', False)

    def readMedicationDosesFromDatabase(self, toDay):
        from adapters.database.medication_db import Medication
        medication = Medication.get_by_id(Medication, toDay)
        doses = {}
        for i in medication:
            day = medication.get('day')
            if day == toDay:
                doses.update({f"dose_{i}": medication.get(f"dose_{i}"), f"scheduled_{i}": medication.get(f"scheduled_{i}")})
        return doses

    def sendMedicationDosesStatusToDatabase(self,medication_id, dose_id, ):
        from adapters.database.medication_db import Medication
        medication = Medication.get_by_id(Medication, medication_id)
        medication.set(f'scheduled_{dose_id}', False)

    def readTasksFromDatabase(self):
        from adapters.database.task_db import Task
        allTasks = Task.query.all()
        tasks = {}
        for i in allTasks:
            scheduled = allTasks.get('scheduled')
            if scheduled:
                tasks.update({"name" : allTasks.get('name'), "time": allTasks.get('time')})
        return tasks

    def taskDone(self, name, time):
        from adapters.database.task_db import Task
        tasks = Task.query.all()
        if tasks.get('name') == name and tasks.get('time') == time:
            tasks.set('scheduled', False)
'''
    def readVisteStatusFromDatabase(self):
        from adapters.database.autodoorlock_db import AutoDoorLock
        variable = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        status = variable.get('status')
        return status

    def sendVisteStatusToDatabase(self, status):
        from adapters.database.autodoorlock_db import AutoDoorLock
        autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        autodoorlock.set('status', status)

'''