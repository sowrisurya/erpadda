# -*- coding: utf-8 -*-
# Copyright (c) 2018, VMRaid Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import vmraid
import unittest

test_dependencies = ["Employee Onboarding"]

class TestEmployeeSeparation(unittest.TestCase):
	def test_employee_separation(self):
		employee = vmraid.db.get_value("Employee", {"status": "Active"})
		separation = vmraid.new_doc('Employee Separation')
		separation.employee = employee
		separation.company = '_Test Company'
		separation.append('activities', {
			'activity_name': 'Deactivate Employee',
			'role': 'HR User'
		})
		separation.boarding_status = 'Pending'
		separation.insert()
		separation.submit()
		self.assertEqual(separation.docstatus, 1)
		separation.cancel()
		self.assertEqual(separation.project, "")