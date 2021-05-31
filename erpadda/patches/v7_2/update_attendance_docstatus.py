from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("education", "doctype", "student_attendance")
	vmraid.db.sql('''
		update `tabStudent Attendance` set
			docstatus=0
		where
			docstatus=1''')