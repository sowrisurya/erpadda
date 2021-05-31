from __future__ import unicode_literals
import vmraid

def execute():
	# 'Schools' module changed to the 'Education'
	# vmraid.reload_doc('schools', 'doctype', 'student_group_student')

	vmraid.reload_doc('education', 'doctype', 'student_group_student')
	vmraid.db.sql("update `tabStudent Group Student` set active=1")
