import datetime
import os
import sys


from collections import OrderedDict

from worklog_db import db, EmpLog


time_spent = EmpLog.time_spent
emp_name = EmpLog.employee_name
task_title = EmpLog.title
task_notes = EmpLog.task_notes
task_date = EmpLog.task_date


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
        for i in output:
            print(i, 'Minutes')

    elif type == 'date':
        entries = list(EmpLog.select().order_by(EmpLog.time_spent.desc()))
        for i in range(0, len(entries)):
            if entries[i].task_date not in output:
                format_date = entries[i].task_date.strftime('%D/%M/%Y')
                output.append(format_date)
            else:
                pass
        print("Available Dates:")
        for i in output:
            print(i)

    elif type == 'employee':
        entries = list(EmpLog.select().order_by(EmpLog.time_spent.desc()))
        for i in range(0, len(entries)):
            if entries[i].employee_name not in output:
                output.append(entries[i].employee_name)
            else:
                pass
        print("Employee Names:")
        for i in output:
            print(i)

    else:
        print("Please choose a valid Type")


def show(logs):
    for entry in logs:
        timestamp = entry.task_date.strftime('%A %B %d, %Y %I:%M%p')
        clear()
        print(timestamp)
        print("="*len(timestamp)+'\n\n')
        print('Employee:   ',entry.employee_name)
        print('Task Title: ',entry.title)
        print('Task Notes: ',entry.task_notes)
        print('Time Spent: ',entry.time_spent)
        print('\n\n'+'='*len(timestamp))
        print('n) for next entry')
        print('d) delete entry')
        print('q) return to main menu')

        next_action = input("Action: [Ndq] ").lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)

def delete_entry(entry):
    """delete an entry"""
    if input("Are you sure?  [yN] ").lower() == 'y':
        entry.delete_instance()
        print("entry deleted!")


def find_int_entries(type, num):
    emp_entries = EmpLog.select().order_by(EmpLog.time_spent.desc())
    if num:
        emp_entries = emp_entries.where(type == num)
    return emp_entries


def find_string_entries(type, arg):
    emp_entries = EmpLog.select().order_by(EmpLog.time_spent.desc())
    if type and arg:
        emp_entries = emp_entries.where(type.contains(arg))
    return emp_entries


app_menu = OrderedDict([
    ('Add Work Entry', add_log),
    ('Find Work Entry ', ),

])

def find_entries(type):



if __name__ == '__main__':
    initialize()
    my_entries = find_string_entries(emp_name, 'James')
    show(find_int_entries(time_spent, 50))
