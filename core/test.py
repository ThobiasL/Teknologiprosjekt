from services.test import Headunit

db = Headunit()

while True:
    
    doorlock = db.readVariableStatusFromDatabase()