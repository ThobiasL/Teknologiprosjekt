# services/test.py
class Headunit:
    def __init__(self):
        pass

    def readVariableStatusFromDatabase(self):
        # Import `AutoDoorLock` dynamically here
        from adapters.database.autodoorlock_db import AutoDoorLock
        autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
        return autodoorlock.get('status')
