class Headunit:
    def __init__(self):
        from application import create_app  # Dynamisk import
        self.app = create_app()

    def readVariableStatusFromDatabase(self):
        try:
            with self.app.app_context():
                from adapters.database.autodoorlock_db import AutoDoorLock
                autodoorlock = AutoDoorLock.query.get(1)
                if autodoorlock:
                    return autodoorlock.status
                return None
        except Exception as e:
            print(f"Feil ved henting av AutoDoorLock: {e}")
            return None
