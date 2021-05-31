# -*- coding: utf-8 -*-
# Copyright (c) 2018, VMRaid Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals
import vmraid
import unittest
from erpadda.hr.doctype.employee.test_employee import make_employee

class TestEmployeeGroup(unittest.TestCase):
	pass

def make_employee_group():
	employee = make_employee("testemployee@example.com")
	employee_group = vmraid.get_doc({
		"doctype": "Employee Group",
		"employee_group_name": "_Test Employee Group",
		"employee_list": [
			{
				"employee": employee
			}
		]
	})
	employee_group_exist = vmraid.db.exists("Employee Group", "_Test Employee Group")
	if not employee_group_exist:
		employee_group.insert()
		return employee_group.employee_group_name
	else:
		return employee_group_exist

def get_employee_group():
	employee_group = vmraid.db.exists("Employee Group", "_Test Employee Group")
	return employee_group