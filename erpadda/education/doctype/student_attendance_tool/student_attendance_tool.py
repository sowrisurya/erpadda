# -*- coding: utf-8 -*-
# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.model.document import Document

class StudentAttendanceTool(Document):
	pass

@vmraid.whitelist()
def get_student_attendance_records(based_on, date=None, student_group=None, course_schedule=None):
	student_list = []
	student_attendance_list = []

	if based_on=="Course Schedule":
		student_group = vmraid.db.get_value("Course Schedule", course_schedule, "student_group")
		if student_group:
			student_list = vmraid.get_list("Student Group Student", fields=["student", "student_name", "group_roll_number"] , \
			filters={"parent": student_group, "active": 1}, order_by= "group_roll_number")

	if not student_list:
		student_list = vmraid.get_list("Student Group Student", fields=["student", "student_name", "group_roll_number"] ,
			filters={"parent": student_group, "active": 1}, order_by= "group_roll_number")

	if course_schedule:
		student_attendance_list= vmraid.db.sql('''select student, status from `tabStudent Attendance` where \
			course_schedule= %s''', (course_schedule), as_dict=1)
	else:
		student_attendance_list= vmraid.db.sql('''select student, status from `tabStudent Attendance` where \
			student_group= %s and date= %s and \
			(course_schedule is Null or course_schedule='')''',
			(student_group, date), as_dict=1)

	for attendance in student_attendance_list:
		for student in student_list:
			if student.student == attendance.student:
				student.status = attendance.status

	return student_list