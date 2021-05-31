# -*- coding: utf-8 -*-
# Copyright (c) 2018, VMRaid Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import vmraid
import unittest
from vmraid.utils import nowdate
from datetime import date

test_dependencies = ["Employee"]

class TestAttendanceRequest(unittest.TestCase):
	def setUp(self):
		for doctype in ["Attendance Request", "Attendance"]:
			vmraid.db.sql("delete from `tab{doctype}`".format(doctype=doctype))

	def test_on_duty_attendance_request(self):
		today = nowdate()
		employee = get_employee()
		attendance_request = vmraid.new_doc("Attendance Request")
		attendance_request.employee = employee.name
		attendance_request.from_date = date(date.today().year, 1, 1)
		attendance_request.to_date = date(date.today().year, 1, 2)
		attendance_request.reason = "On Duty"
		attendance_request.company = "_Test Company"
		attendance_request.insert()
		attendance_request.submit()
		attendance = vmraid.get_doc('Attendance', {
			'employee': employee.name,
			'attendance_date': date(date.today().year, 1, 1),
			'docstatus': 1
		})
		self.assertEqual(attendance.status, 'Present')
		attendance_request.cancel()
		attendance.reload()
		self.assertEqual(attendance.docstatus, 2)

	def test_work_from_home_attendance_request(self):
		today = nowdate()
		employee = get_employee()
		attendance_request = vmraid.new_doc("Attendance Request")
		attendance_request.employee = employee.name
		attendance_request.from_date = date(date.today().year, 1, 1)
		attendance_request.to_date = date(date.today().year, 1, 2)
		attendance_request.reason = "Work From Home"
		attendance_request.company = "_Test Company"
		attendance_request.insert()
		attendance_request.submit()
		attendance = vmraid.get_doc('Attendance', {
			'employee': employee.name,
			'attendance_date': date(date.today().year, 1, 1),
			'docstatus': 1
		})
		self.assertEqual(attendance.status, 'Work From Home')
		attendance_request.cancel()
		attendance.reload()
		self.assertEqual(attendance.docstatus, 2)

def get_employee():
	return vmraid.get_doc("Employee", "_T-Employee-00001")
