from adapters.database.autodoorlock_db import AutoDoorLock
from adapters.database.medication_db import Medication
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

    def readMedicationDosesFromDatabase(self, day):
        medication = Medication.get_by_id(Medication, day)
        doses = [
            {
                'dose_id': i,
                'time': medication.get(f'dose_{i}'),
                'scheduled': medication.get(f'scheduled_{i}')
            } for i in range(1, 5)
        ]
        return doses

    def sendMedicationDosesStatusToDatabase(self,medication_id, dose_id, ):
        medication = Medication.get_by_id(Medication, medication_id)
        medication.set(f'scheduled_{dose_id}', False)

    def readVisteStatusFromDatabase(self):
        variable = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        status = variable.get('status')
        return status

    def sendVisteStatusToDatabase(self, status):
        autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        autodoorlock.set('status', status)

    def readGoForAWalk(self):
        go_for_a_walk = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        time = go_for_a_walk.get('time')
        return time

    def readEatDinner(self):
        eat_dinner = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        time = eat_dinner.get('time')
        return time

