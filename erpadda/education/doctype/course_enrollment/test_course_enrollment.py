# -*- coding: utf-8 -*-
# Copyright (c) 2018, VMRaid Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import vmraid
import unittest


from erpadda.education.doctype.student.test_student import create_student
from erpadda.education.doctype.student.test_student import get_student
from erpadda.education.doctype.program.test_program import setup_program
from erpadda.education.doctype.course_activity.test_course_activity import make_course_activity

class TestCourseEnrollment(unittest.TestCase):
	def setUp(self):
		setup_program()
		student = create_student({"first_name": "_Test First", "last_name": "_Test Last", "email": "_test_student_1@example.com"})
		program_enrollment = student.enroll_in_program("_Test Program")
		course_enrollment = vmraid.db.get_value("Course Enrollment",
			{"course": "_Test Course 1", "student": student.name, "program_enrollment": program_enrollment.name}, 'name')
		make_course_activity(course_enrollment, "Article", "_Test Article 1-1")

	def test_get_progress(self):
		student = get_student("_test_student_1@example.com")
		program_enrollment_name = vmraid.get_list("Program Enrollment", filters={"student": student.name, "Program": "_Test Program"})[0].name
		course_enrollment_name = vmraid.get_list("Course Enrollment", filters={"student": student.name, "course": "_Test Course 1", "program_enrollment": program_enrollment_name})[0].name
		course_enrollment = vmraid.get_doc("Course Enrollment", course_enrollment_name)
		progress = course_enrollment.get_progress(student)
		finished = {'content': '_Test Article 1-1', 'content_type': 'Article', 'is_complete': True}
		self.assertTrue(finished in progress)
		vmraid.db.rollback()

	def tearDown(self):
		for entry in vmraid.db.get_all("Course Enrollment"):
			vmraid.delete_doc("Course Enrollment", entry.name)

		for entry in vmraid.db.get_all("Program Enrollment"):
			doc = vmraid.get_doc("Program Enrollment", entry.name)
			doc.cancel()
			doc.delete()



