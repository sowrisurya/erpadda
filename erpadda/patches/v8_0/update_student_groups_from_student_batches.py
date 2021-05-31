# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.model.utils.rename_field import *
from vmraid.model.mapper import get_mapped_doc


def execute():
	if vmraid.db.table_exists("Student Batch"):
		student_batches = vmraid.db.sql('''select name from `tabStudent Batch`''', as_dict=1)

		for student_batch in student_batches:
			if vmraid.db.exists("Student Group", student_batch.get("name")):
				student_group = vmraid.get_doc("Student Group", student_batch.get("name"))

				if vmraid.db.table_exists("Student Batch Student"):
					current_student_list = vmraid.db.sql_list('''select student from `tabStudent Group Student`
						where parent=%s''', (student_group.name))
					batch_student_list = vmraid.db.sql_list('''select student from `tabStudent Batch Student`
						where parent=%s''', (student_group.name))

					student_list = list(set(batch_student_list)-set(current_student_list))
					if student_list:
						student_group.extend("students", [{"student":d} for d in student_list])

				if vmraid.db.table_exists("Student Batch Instructor"):
					current_instructor_list = vmraid.db.sql_list('''select instructor from `tabStudent Group Instructor`
						where parent=%s''', (student_group.name))
					batch_instructor_list = vmraid.db.sql_list('''select instructor from `tabStudent Batch Instructor`
						where parent=%s''', (student_group.name))

					instructor_list = list(set(batch_instructor_list)-set(current_instructor_list))
					if instructor_list:
						student_group.extend("instructors", [{"instructor":d} for d in instructor_list])

				student_group.save()
