# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.model.utils.rename_field import *
from vmraid.model.mapper import get_mapped_doc


def execute():
	# for converting student batch into student group
	for doctype in ["Student Group", "Student Group Student", 'Program Enrollment',
		"Student Group Instructor", "Student Attendance", "Student", "Student Batch Name"]:
		# 'Schools' module changed to the 'Education'
		# vmraid.reload_doc("schools", "doctype", vmraid.scrub(doctype))

		vmraid.reload_doc("education", "doctype", vmraid.scrub(doctype))

	if vmraid.db.table_exists("Student Batch"):
		student_batches = vmraid.db.sql('''select name as student_group_name, student_batch_name as batch,
			program, academic_year, academic_term from `tabStudent Batch`''', as_dict=1)

		for student_batch in student_batches:
			# create student batch name if does not exists !!
			if student_batch.get("batch") and not vmraid.db.exists("Student Batch Name", student_batch.get("batch")):
				vmraid.get_doc({
					"doctype": "Student Batch Name",
					"batch_name": student_batch.get("batch")
				}).insert(ignore_permissions=True)

			student_batch.update({"doctype":"Student Group", "group_based_on": "Batch"})
			doc = vmraid.get_doc(student_batch)

			if vmraid.db.sql("SHOW COLUMNS FROM `tabStudent Batch Student` LIKE 'active'"):
				cond = ", active"
			else:
				cond = " "
			student_list = vmraid.db.sql('''select student, student_name {cond} from `tabStudent Batch Student`
				where parent=%s'''.format(cond=cond), (doc.student_group_name), as_dict=1)

			if student_list:
				for i, student in enumerate(student_list):
					student.update({"group_roll_number": i+1})
				doc.extend("students", student_list)

			instructor_list = None
			if vmraid.db.table_exists("Student Batch Instructor"):
				instructor_list = vmraid.db.sql('''select instructor, instructor_name from `tabStudent Batch Instructor`
					where parent=%s''', (doc.student_group_name), as_dict=1)
			if instructor_list:
				doc.extend("instructors", instructor_list)
			doc.save()

	# delete the student batch and child-table
	if vmraid.db.table_exists("Student Batch"):
		vmraid.delete_doc("DocType", "Student Batch", force=1)
	if vmraid.db.table_exists("Student Batch Student"):
		vmraid.delete_doc("DocType", "Student Batch Student", force=1)
	if vmraid.db.table_exists("Student Batch Instructor"):
		vmraid.delete_doc("DocType", "Student Batch Instructor", force=1)

	# delete the student batch creation tool
	if vmraid.db.table_exists("Student Batch Creation Tool"):
		vmraid.delete_doc("DocType", "Student Batch Creation Tool", force=1)

	# delete the student batch creation tool
	if vmraid.db.table_exists("Attendance Tool Student"):
		vmraid.delete_doc("DocType", "Attendance Tool Student", force=1)

	# change the student batch to student group in the student attendance
	table_columns = vmraid.db.get_table_columns("Student Attendance")
	if "student_batch" in table_columns:
		rename_field("Student Attendance", "student_batch", "student_group")
