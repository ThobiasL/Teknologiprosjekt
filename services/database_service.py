from application.database import db


def get_autodoorlock_status():
    try:
        from adapters.database.autodoorlock_db import AutoDoorLock  # Dynamisk import
        autodoorlock = AutoDoorLock.query.get(1)
        if autodoorlock:
            return autodoorlock.status
        return None
    except ImportError as e:
        print(f"Feil ved import av AutoDoorLock: {e}")
        return None
    except Exception as e:
        print(f"Feil ved henting av AutoDoorLock: {e}")
        return None
