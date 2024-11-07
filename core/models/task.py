from application import db

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=True)
    scheduled = db.Column(db.Boolean, nullable=False, default=False)

    def enable(self):
        self.scheduled = True

    def disable(self):
        self.scheduled = False

    def set_time(self, time):
        self.time = time
    
    def get_time(self):
        return self.time