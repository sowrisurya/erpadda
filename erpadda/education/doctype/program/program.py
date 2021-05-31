# -*- coding: utf-8 -*-
# Copyright (c) 2015, VMRaid Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.model.document import Document

class Program(Document):

	def get_course_list(self):
		program_course_list = self.courses
		course_list = [vmraid.get_doc("Course", program_course.course) for program_course in program_course_list]
		return course_list