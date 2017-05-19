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
    employee_name = input("Enter employee name:  ")
    date = datetime.datetime.now()
    task_title = input("title:  ")
    task_time = int(input("time spent:  "))
    new_notes = input("Notes: ")
    EmpLog.create(employee_name=employee_name,
                  task_date=date,
                  title=task_title,
                  time_spent=task_time,
                  task_notes=new_notes)


def delete_entry(entry):
    """delete an entry"""
    if input("Are you sure?  [yN] ").lower() == 'y':
        entry.delete_instance()
        print("entry deleted!")


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
                fmt_date = entries[i].task_date.strftime("%m/%d/%Y")
                if fmt_date not in output:
                    output.append(fmt_date)
                else:
                    continue
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


def find_time_spent(num):
    emp_entries = EmpLog.select().order_by(EmpLog.time_spent.desc())
    if num:
        emp_entries = emp_entries.where(EmpLog.time_spent == num)
    return emp_entries


def find_emp_name(arg):
    emp_entries = EmpLog.select().order_by(EmpLog.time_spent.desc())
    if arg:
        emp_entries = emp_entries.where(EmpLog.employee_name.contains(arg))
    return emp_entries


def find_title_query(query):
    emp_entries = EmpLog.select().order_by(EmpLog.time_spent.desc())
    if query:
        emp_entries = emp_entries.where(EmpLog.title.contains(query))
    return emp_entries


def find_notes_query(query):
    emp_entries = EmpLog.select().order_by(EmpLog.time_spent.desc())
    if query:
        emp_entries = emp_entries.where(EmpLog.task_notes.contains(query))
    return emp_entries


def find_by_date(date): #TODO Need to fix
    pass



def show(logs):
    for entry in logs:
        timestamp = entry.task_date.strftime("%A %B %d, %Y %I:%M%p")
        clear()
        print('*'*len(timestamp))
        print('\n',timestamp)
        print("="*len(timestamp)+'\n')
        print('Employee:   ',entry.employee_name)
        print('Task Title: ',entry.title)
        print('Task Notes: ',entry.task_notes)
        print('Time Spent: ',entry.time_spent)
        print('\n'+'='*len(timestamp))
        print('n) for next entry')
        print('d) delete entry')
        print('q) return to main menu')

        next_action = input("Action: [Ndq] ").lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)

"""
app_menu = OrderedDict([
    ('Add Work Entry', add_log),
    ('Find Work Entry ', find_entries),

])
"""

def find_entries():
    type = input("How would you like to find work entries?: "
                 "1: By Employee Name, "
                 "2: By Date, "
                 "3: By Time Spent, "
                 "4: By Search Query  ")
    if type == '1':
        name = input("What is the Employees Name?  ")
        pass


if __name__ == '__main__':
    initialize()
    #my_entries = find_string_entries(emp_name, 'James')
    #print(find_emp_name("James"))
    #add_log()
    #show(find_by_date('05/19/2017'))


