# services/database_operations.py
from adapters.database.autodoorlock_db import AutoDoorLock
from adapters.database.medication_db import Medication
from adapters.database.task_db import Task

class DatabaseOperations:
    @staticmethod
    def get_auto_door_lock_status():
        return AutoDoorLock.get_by_id(AutoDoorLock, 1).get('status')

    @staticmethod
    def set_auto_door_lock_status(status):
        lock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        lock.set('status', status)
        lock.save()
    
    @staticmethod
    def get_all_tasks():
        return Task.query.all()

    @staticmethod
    def mark_task_done(name, time):
        task = Task.query.filter_by(name=name, time=time).first()
        if task:
            task.set('scheduled', False)
            task.save()
