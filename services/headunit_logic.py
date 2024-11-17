# services/headunit_logic.py
from services.database_operations import DatabaseOperations

class HeadunitLogic:
    def readVariableStatusFromDatabase(self):
        return DatabaseOperations.get_auto_door_lock_status()

    def sendAutoDoorLockTimeToDatabase(self, status):
        DatabaseOperations.set_auto_door_lock_status(status)

    def readTasksFromDatabase(self):
        tasks = DatabaseOperations.get_all_tasks()
        return [{"name": task.get('name'), "time": task.get('time')} for task in tasks]

    def taskDone(self, name, time):
        DatabaseOperations.mark_task_done(name, time)
