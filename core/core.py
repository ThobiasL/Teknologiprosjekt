def main():
    from services.test import Headunit  # Dynamisk import
    db = Headunit()

    while True:
        try:
            doorlock_status = db.readVariableStatusFromDatabase()
            print(f"Doorlock status: {doorlock_status}")
        except Exception as e:
            print(f"Feil under henting av dørlåsstatus: {e}")
            break

if __name__ == "__main__":
    main()
