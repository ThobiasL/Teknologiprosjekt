from application.database import db
from adapters.database.base import Base
from time import sleep

class Headunit(Base):
    def __init__(self, variable, reminders):
        self.variable = variable
        self.reminders = {"go_for_a_walk": "", "pill_dispensation": "", "eat_dinner": ""}

    def readVariableFromDatabase(self, variable):

        valueOfVariable = ""
        return valueOfVariable

    def reminder(self):
        for value in self.reminders.values():
            self.reminders.update({self.reminders.values(): self.readVariableFromDatabase(self.reminders.keys())})

        return self.reminders

    def updateReminder(self, variable):
        self.reminders.update({variable : ""})

    def sendInfoToDatabase(self, variable, value):
        db.sendInfoToDatabase(variable, value)

    def sendPillsDropedToDatabase(self, variable, value, time):
