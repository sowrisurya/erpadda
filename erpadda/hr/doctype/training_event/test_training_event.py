# -*- coding: utf-8 -*-
# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import vmraid
import unittest
from vmraid.utils import today, add_days
from erpadda.payroll.doctype.salary_structure.test_salary_structure import make_employee

class TestTrainingEvent(unittest.TestCase):
	def setUp(self):
		create_training_program("Basic Training")
		self.employee = make_employee("robert_loan@trainig.com")
		self.employee2 = make_employee("suzie.tan@trainig.com")

	def test_create_training_event(self):
		if not vmraid.db.get_value("Training Event", "Basic Training Event"):
			vmraid.get_doc({
				"doctype": "Training Event",
				"event_name": "Basic Training Event",
				"training_program": "Basic Training",
				"location": "Union Square",
				"start_time": add_days(today(), 5),
				"end_time": add_days(today(), 6),
				"introduction": "Welcome to the Basic Training Event",
				"employees": get_attendees(self.employee, self.employee2)
			}).insert()

def create_training_program(training_program):
	if not vmraid.db.get_value("Training Program", training_program):
		vmraid.get_doc({
			"doctype": "Training Program",
			"training_program": training_program,
			"description": training_program
		}).insert()

def get_attendees(employee, employee2):
	return [
		{"employee": employee},
		{"employee": employee2}
	]