import datetime
import os
import sys


from collections import OrderedDict

from worklog_db import db, EmpLog


def initialize():
    """Create the database and the table if they don't exits."""
    db.create_tables([EmpLog], safe=True)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def add_log():
    date = datetime.datetime.now
    employee_name = input("Enter employee name:  ")
    task_title = input("title:  ")
    task_time = int(input("time spent:  "))
    new_notes = input("Notes: ")
    EmpLog.create(employee_name=employee_name,
                  task_date=date(),
                  title=task_title,
                  time_spent=task_time,
                  task_notes=new_notes)


def show_available(type):
    output = []
    if type == 'time':
        entries = list(EmpLog.select().order_by(EmpLog.time_spent.desc()))
        for i in range(0, len(entries)):
            if entries[i].time_spent not in output:
                output.append(entries[i].time_spent)
            else:
                pass
        return output

    elif type == 'date': # @TODO format datetime.datetime before returning..
        entries = list(EmpLog.select().order_by(EmpLog.time_spent.desc()))
        for i in range(0, len(entries)):
            if entries[i].task_date not in output:
                output.append(entries[i].task_date)
            else:
                pass
        return output

    elif type == 'employee':
        entries = list(EmpLog.select().order_by(EmpLog.time_spent.desc()))
        for i in range(0, len(entries)):
            if entries[i].employee_name not in output:
                output.append(entries[i].employee_name)
            else:
                pass
        return output

    else:
        print("Please choose a valid Type")


def show(logs):
    pass


def find_by_employee(name):
    pass


def find_by_date(date):
    pass


def find_by_time(num):
    pass


def find_by_query(query):
    pass

if __name__ == '__main__':
    initialize()
    #add_log()
    print(show_available('time'))
