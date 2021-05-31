# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid



def get_context(context):
	course = vmraid.get_doc('Course', vmraid.form_dict.course)
	sidebar_title = course.name

	context.no_cache = 1
	context.show_sidebar = True
	course = vmraid.get_doc('Course', vmraid.form_dict.course)
	course.has_permission('read')
	context.doc = course
	context.sidebar_title = sidebar_title
	context.intro = course.course_intro

