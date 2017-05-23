import datetime

from peewee import *

db = SqliteDatabase('work_log.db')


class EmpLog(Model):
    employee_name = CharField(max_length=255)
    task_date = DateTimeField(default=datetime.datetime.now())
    title = CharField(max_length=255)
    time_spent = IntegerField()
    task_notes = TextField()

    class Meta:
        database = db

