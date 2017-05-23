import datetime

from worklog_db import EmpLog


class GetLogs():
    def __init__(self):
        pass

    def time_spent(self, num):
        emp_entries = EmpLog.select().order_by(EmpLog.time_spent.desc())
        if num:
            emp_entries = emp_entries.where(EmpLog.time_spent == num)
        return emp_entries

    def emp_name(self, arg):
        emp_entries = EmpLog.select().order_by(EmpLog.time_spent.desc())
        if arg:
            emp_entries = emp_entries.where(EmpLog.employee_name.contains(arg))
        return emp_entries

    def by_query(self, query):  #TODO Need to fix
        emp_entries = EmpLog.select()
        if query:
            emp_entries = emp_entries.where(EmpLog.title.contains(query),
                                            EmpLog.task_notes.contains(query))
        return emp_entries

    def by_date(self, day, month, year):  # TODO Need to fix
        input_date = datetime.date(year=year, month=month, day=day)
        emp_entries = EmpLog.select()
        if day and month and year:
            emp_entries = emp_entries.where(EmpLog.task_date.month == input_date.month and
                                            EmpLog.task_date.year == input_date.year and
                                            EmpLog.task_date.day == input_date.day)
            return emp_entries
