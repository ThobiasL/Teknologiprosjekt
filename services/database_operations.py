# services/database_operations.py

from adapters.database.autodoorlock_db import AutoDoorLock
from adapters.database.medication_db import Medication
from adapters.database.task_db import Task

class DatabaseOperations:
    @staticmethod
    def get_auto_door_lock_status():
        autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        return autodoorlock.get('status')

    @staticmethod
    def set_auto_door_lock_status(status):
        autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        autodoorlock.set('status', status)

    @staticmethod
    def get_auto_door_lock_time():
        autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        return autodoorlock.get('time')

    @staticmethod
    def get_medication_doses(day):
        medication = Medication.get_by_id(Medication, day)
        doses = {}
        for i in medication:
            day = medication.get('day')
            if day == day:
                doses.update({
                    f"dose_{i}": medication.get(f"dose_{i}"),
                    f"scheduled_{i}": medication.get(f"scheduled_{i}")
                })
        return doses

    @staticmethod
    def set_medication_dose_status(medication_id, dose_id):
        medication = Medication.get_by_id(Medication, medication_id)
        medication.set(f'scheduled_{dose_id}', False)

    @staticmethod
    def get_all_tasks():
        all_tasks = Task.query.all()
        tasks = []
        for task in all_tasks:
            tasks.append({
                "name": task.get('name'),
                "time": task.get('time'),
                "scheduled": task.get('scheduled')
            })
        return tasks

    @staticmethod
    def mark_task_done(task_name, task_time):
        task = Task.query.filter_by(name=task_name, time=task_time).first()
        if task:
            task.set('scheduled', False)
