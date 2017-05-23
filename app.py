import datetime
import os
import sys

from collections import OrderedDict
from worklog_db import db, EmpLog
from get_logs import GetLogs

get = GetLogs()


def initialize():
    """Create the database and the table if they don't exits."""
    db.create_tables([EmpLog], safe=True)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def add_log():
    """Add a new entry to the Work Log"""
    print("Add a new entry to the Work Log")
    employee_name = input("Enter employee name:  ").lower().strip()
    date = datetime.datetime.now()
    task_title = input("Task Title:  ").lower().strip()
    task_time = int(input("Time Spent [minutes only]:  "))
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
                show(get.time_spent(choice))
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
    print("Enter 'b' at anytime to go back")

    count = 0
    while len(output) > 0:
        if count <= 0:
            month = int(input("Enter two digit month:  "))
            day = int(input("Enter two digit day:  "))
            year = int(input("Enter two digit year:  "))
        else:
            clear()
            print("No more entries found. Please choose another or 'b' to go back to search menu")
            show_available_dates()
        if day or month or year != 'b':
            count += 1
            date_logs = get.by_date(year=year, month=month, day=day)
            show(date_logs)
        else:
            find_menu_loop()
    else:
        choice = input("No entries found. Select 'b' to go back:  ")
        if choice:
            find_menu_loop()


def show_available_emp():
    """Show Employee Names"""
    output = []
    entries = list(EmpLog.select().order_by(EmpLog.time_spent.desc()))
    for i in range(0, len(entries)):
        if entries[i].employee_name not in output:
            output.append(entries[i].employee_name)
        else:
            pass

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
                emp_logs = get.emp_name(choice)
                show(emp_logs)
            else:
                continue
        else:
            find_menu_loop()
    else:
        choice = input("No entries found. Select 'b' to go back:  ")
        if choice:
            find_menu_loop()


def get_query():
    """Search by Query"""
    clear()
    query = input("Please type your query:  ").lower().strip()
    query_logs = [get.by_query(query)]
    return query_logs


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
    ('s', get_query),
])


if __name__ == '__main__':
    initialize()
    menu_loop()
    #find_by_date()
    #test = get.by_query('trafsda')
    #print(test)




