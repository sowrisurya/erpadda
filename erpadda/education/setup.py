# -*- coding: utf-8 -*-
# Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import vmraid
from erpadda.setup.utils import insert_record


def setup_education():
	disable_desk_access_for_student_role()
	if vmraid.db.exists("Academic Year", "2015-16"):
		# already setup
		return
	create_academic_sessions()

def create_academic_sessions():
	data = [
		{"doctype": "Academic Year", "academic_year_name": "2015-16"},
		{"doctype": "Academic Year", "academic_year_name": "2016-17"},
		{"doctype": "Academic Year", "academic_year_name": "2017-18"},
		{"doctype": "Academic Year", "academic_year_name": "2018-19"},
		{"doctype": "Academic Term", "academic_year": "2016-17", "term_name": "Semester 1"},
		{"doctype": "Academic Term", "academic_year": "2016-17", "term_name": "Semester 2"},
		{"doctype": "Academic Term", "academic_year": "2017-18", "term_name": "Semester 1"},
		{"doctype": "Academic Term", "academic_year": "2017-18", "term_name": "Semester 2"}
	]
	insert_record(data)

def disable_desk_access_for_student_role():
	try:
		student_role = vmraid.get_doc("Role", "Student")
	except vmraid.DoesNotExistError:
		create_student_role()
		return

	student_role.desk_access = 0
	student_role.save()

def create_student_role():
	student_role = vmraid.get_doc({
		"doctype": "Role",
		"role_name": "Student",
		"desk_access": 0,
		"restrict_to_domain": "Education"
	})
	student_role.insert()
