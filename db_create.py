__author__ = 'Beryl'
#DB create
from views import db
from models import Task
from datetime import date


db.create_all()
db.session.add(Task("Finish this tutorial", date(2014, 3, 13), 10, 1))
db.session.add(Task("Finish Real Python Course 2", date(2014, 3, 13), 10, 1))
db.session.commit()
