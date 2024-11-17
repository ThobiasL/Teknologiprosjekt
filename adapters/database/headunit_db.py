from adapters.database.autodoorlock_db import AutoDoorLock
from adapters.database.medication_db import Medication
from adapters.database.task_db import Task
from adapters.database.base import Base


class Headunit(Base):
    def __init__(self):
        pass

    def readVariableStatusFromDatabase(self):
        autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        status = autodoorlock.get('status')
        return status

    def readAutoDoorLockTimeFromDatabase(self):
        autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        time = autodoorlock.get('time')
        return time

    def sendAutoDoorLockTimeToDatabase(self, status):
        autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        if status == 1:
            autodoorlock.set('status', True)
        elif status == 0:
            autodoorlock.set('status', False)

    def readMedicationDosesFromDatabase(self, toDay):
        medication = Medication.get_by_id(Medication, toDay)
        doses = {}
        for i in medication:
            day = medication.get('day')
            if day == toDay:
                doses.update({f"dose_{i}": medication.get(f"dose_{i}"), f"scheduled_{i}": medication.get(f"scheduled_{i}")})
        return doses

        #doses = [
        #    {
        #        'dose_id': i,
        #        'time': medication.get(f'dose_{i}'),
        #        'scheduled': medication.get(f'scheduled_{i}')
        #    } for i in range(1, 5)
        #]
        #return doses

    def sendMedicationDosesStatusToDatabase(self,medication_id, dose_id, ):
        medication = Medication.get_by_id(Medication, medication_id)
        medication.set(f'scheduled_{dose_id}', False)

    def readTasksFromDatabase(self):
        allTasks = AutoDoorLock.query.all()
        tasks = {}
        for i in allTasks:
            scheduled = allTasks.get('scheduled')
            if scheduled:
                tasks.update({"name" : allTasks.get('name'), "time": allTasks.get('time')})
        return tasks

    def taskDone(self, name, time):
        tasks = AutoDoorLock.query.all()
        if tasks.get('name') == name and tasks.get('time') == time:
            tasks.set('scheduled', False)

    def readVisteStatusFromDatabase(self):
        variable = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        status = variable.get('status')
        return status

    def sendVisteStatusToDatabase(self, status):
        autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        autodoorlock.set('status', status)
