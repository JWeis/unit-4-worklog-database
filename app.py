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


def add_log():
    """Add a new entry to the Work Log"""
    print("Add a new entry to the Work Log")
    employee_name = input("Enter employee name:  ").lower().strip()
    date = datetime.datetime.now()
    task_title = input("Task Title:  ").lower().strip()
    task_time = int(input("Time Spent:  "))
    new_notes = input("Notes: ").lower().strip()
    EmpLog.create(employee_name=employee_name,
                  task_date=date,
                  title=task_title,
                  time_spent=task_time,
                  task_notes=new_notes)
    clear()
    print("Task added successfully!")
    next_action = input("a) Add another entry\n"
                        "b) Back to main menu\n"
                        "Action: ").lower().strip()
    if next_action == "a":
        clear()
        add_log()
    else:
        menu_loop()


def delete_entry(entry):
    """Delete This Entry"""
    if input("Are you sure?  [yN] ").lower() == 'y':
        entry.delete_instance()
        print("entry deleted!")


def show_available_time():
    """Show Available Times"""
    output = []
    entries = list(EmpLog.select().order_by(EmpLog.time_spent.desc()))
    for i in range(0, len(entries)):
        if entries[i].time_spent not in output:
            output.append(entries[i].time_spent)
        else:
            pass
    print("Available Times:")
    for i in output:
        print(i, 'Minutes')
    print("Enter 'b' to go back")

    count = 0
    while len(output) > 0:
        if count <= 0:
            choice = input("Please enter a time amount [numbers only]: ")
            try:
                choice = int(choice)
            except ValueError:
                if choice == 'b':
                    find_menu_loop()
                else:
                    print("Please use numbers only or 'b'...")
        else:
            clear()
            print("No more entries found. Please choose another or 'b' to go back to search menu")
            show_available_time()
        if choice != 'b':
            if choice in output:
                count += 1
                show(find_time_spent(choice))
            else:
                continue
        else:
            find_menu_loop()
    else:
        choice = input("No entries found. Select 'b' to go back:  ")
        if choice:
            find_menu_loop()


def show_available_dates():
    """Show Available Dates"""
    output = []
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



def show_available_emp():
    """Show Employee Names"""
    output = []
    entries = list(EmpLog.select().order_by(EmpLog.time_spent.desc()))
    for i in range(0, len(entries)):
        if entries[i].employee_name not in output:
            output.append(entries[i].employee_name)
        else:
            pass
    #clear()
    print("Employee Names:")
    for i in output:
        print(i)
    print("Enter 'b' to go back")
    count = 0
    while len(output) > 0:
        if count <= 0:
            choice = input("Please enter an employee name: ")
        else:
            clear()
            print("No more entries found. Please choose another or 'b' to go back to search menu")
            show_available_emp()
        if choice != 'b':
            if choice in output:
                count += 1
                show(find_emp_name(choice))
            else:
                continue
        else:
            find_menu_loop()
    else:
        choice = input("No entries found. Select 'b' to go back:  ")
        if choice:
            find_menu_loop()


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

        next_action = input("Action: ").lower().strip()
        if next_action == 'q':
            menu_loop()
        elif next_action == 'd':
            delete_entry(entry)


def menu_loop():
    choice = None

    while choice != 'q':
        clear()
        print("Please make a selection")
        print("Enter 'q' to Quit.")
        for key, value in app_menu.items():
            print("{}) {}".format(key, value.__doc__))
        choice = input("Action: ").lower().strip()

        if choice in app_menu:
            clear()
            app_menu[choice]()

        if choice == 'q':
            quit()


def find_menu_loop():
    """Find Entries"""
    choice = None

    while choice != 'b':
        clear()
        print("Choose a method to search entries")
        print("Enter 'b' to go back.")
        for key, value in find_entries_menu.items():
            print("{}) {}".format(key, value.__doc__))
        choice = input("Action: ").lower().strip()

        if choice in find_entries_menu:
            clear()
            find_entries_menu[choice]()
    if choice == 'b':
        menu_loop()


app_menu = OrderedDict([
    ('a', add_log),
    ('f', find_menu_loop),

])

find_entries_menu = OrderedDict([
    ('e', show_available_emp),
    ('d', show_available_dates),
    ('t', show_available_time),
])


if __name__ == '__main__':
    initialize()
    menu_loop()



