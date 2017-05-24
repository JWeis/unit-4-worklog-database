import unittest

from get_logs import GetLogs
from worklog_db import EmpLog


class GetLogTests(unittest.TestCase):
    def test_time_spent(self):
        self.assertTrue(GetLogs.time_spent(self,'s') == AttributeError)

    def test_emp_name(self):
        self.assertTrue(GetLogs.emp_name(self, 5) == AttributeError)

    def test_by_date(self):
        self.assertTrue(GetLogs.by_date(self, year=1800, month=12, day=20) == ValueError)


class WorkLogTests(unittest.TestCase):
    def test_emp_log(self):
        assert EmpLog.employee_name == True
        assert EmpLog.time_spent == True
        assert EmpLog.task_notes == True
        assert EmpLog.title == True


if __name__ == '__main__':
    unittest.main()
