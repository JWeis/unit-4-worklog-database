import datetime
import os

from collections import OrderedDict
from worklog_db import db, EmpLog
from get_logs import GetLogs

get = GetLogs()


def initialize():  # pragma: no cover
    """Create the database and the table if they don't exits."""
    db.create_tables([EmpLog], safe=True)


def clear():  # pragma: no cover
    os.system('cls' if os.name == 'nt' else 'clear')


def add_log():
    """Add a new entry to the Work Log"""
    print("Add a new entry to the Work Log\n")
    employee_name = input("Enter Name:  ").lower().strip()
    date = datetime.datetime.now()
    task_title = input("\nTask Name:  ").lower().strip()
    task_time = int(input("\nTime Spent [minutes only]:  "))
    new_notes = input("\nAdditional Notes: ").lower().strip()

    EmpLog.create(employee_name=employee_name,
                  task_date=date,
                  title=task_title,
                  time_spent=task_time,
                  task_notes=new_notes)

    clear()

    print("*** Task added successfully! ***\n")
    next_action = input("a) Add another entry\n"
                        "b) Back to main menu\n"
                        "\nAction: ").lower().strip()

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

    print("Available Times Spent:\n")
    for i in output:
        print(i, 'Minutes')

    print("\nEnter 'b' to go back")
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
            print("*** No more entries found. Please choose another ***\n "
                  "*** Or 'b' to go back to search menu ***")
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
    show_output=[]
    entries = list(EmpLog.select().order_by(EmpLog.time_spent.desc()))

    for i in range(0, len(entries)):
        if entries[i].task_date not in output or show_output:
            show_output.append(entries[i].task_date)
            fmt_date = entries[i].task_date.strftime("%m/%d/%Y")
            if fmt_date not in output:
                output.append(fmt_date)
            else:
                continue
        else:
            pass

    print("Available Dates:\n")
    for i in output:
        print(i)

    print("\nEnter 'b' at anytime to go back")
    count = 0

    while len(output) > 0:
        try:
            if count <= 0:
                month = input("Enter two digit month:  ")
                if month != 'b':
                    month = int(month)
                else:
                    find_menu_loop()
                day = input("Enter two digit day:  ")
                if day != 'b':
                    day = int(day)
                else:
                    find_menu_loop()
                year = input("Enter four digit year:  ")
                if year != 'b':
                    year = int(year)
                else:
                    find_menu_loop()
                date_logs = get.by_date(year=year, month=month, day=day)
                if date_logs in show_output:
                    count += 1
                    show(date_logs)
            else:
                clear()
                print("*** No more entries found. Please choose another ***\n "
                      "*** Or 'b' to go back to search menu ***")
                show_available_dates()
        except ValueError:
            print("Please follow input instructions...")

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

    print("Employee Names:\n")
    for i in output:
        print(i.capitalize())

    print("\nEnter 'b' to go back")
    count = 0

    while len(output) > 0:
        if count <= 0:
            choice = input("Please enter an employee name: ").lower().strip()
        else:
            clear()
            print("*** No more entries found. Please choose another ***\n "
                  "*** Or 'b' to go back to search menu ***")
            show_available_emp()

        if choice != 'b':
            if choice in output:
                count += 1
                emp_logs = get.emp_name(choice)
                show(emp_logs)
            else:
                print("Please choose a name that is shown above..")
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
        else:
            print("Please chose 'n', 'd' or 'q'..")


def menu_loop():
    choice = None

    while choice != 'q':
        clear()
        print("Please make a selection")
        print("Enter 'q' to Quit0.\n")
        for key, value in app_menu.items():
            print("{}) {}".format(key, value.__doc__))
        choice = input("\nAction: ").lower().strip()

        if choice in app_menu:
            clear()
            app_menu[choice]()

        elif choice == 'q':
            quit()
        else:
            print("Please chose an item from the menu given..")


def find_menu_loop():
    """Find Entries"""
    choice = None

    while choice != 'b':
        clear()
        print("Choose a method to search entries")
        print("Enter 'b' to go back.\n")
        for key, value in find_entries_menu.items():
            print("{}) {}".format(key, value.__doc__))
        choice = input("\nAction: ").lower().strip()

        if choice in find_entries_menu:
            clear()
            find_entries_menu[choice]()
        else:
            print("Please chose an item from the menu given..")
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
