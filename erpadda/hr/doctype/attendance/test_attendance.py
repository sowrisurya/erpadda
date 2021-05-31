# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors and Contributors
# See license.txt
from __future__ import unicode_literals

import vmraid
import unittest
from vmraid.utils import nowdate

test_records = vmraid.get_test_records('Attendance')

class TestAttendance(unittest.TestCase):
	def test_mark_absent(self):
		from erpadda.hr.doctype.employee.test_employee import make_employee
		employee = make_employee("test_mark_absent@example.com")
		date = nowdate()
		vmraid.db.delete('Attendance', {'employee':employee, 'attendance_date':date})
		from erpadda.hr.doctype.attendance.attendance import mark_attendance
		attendance = mark_attendance(employee, date, 'Absent')
		fetch_attendance = vmraid.get_value('Attendance', {'employee':employee, 'attendance_date':date, 'status':'Absent'})
		self.assertEqual(attendance, fetch_attendance)
