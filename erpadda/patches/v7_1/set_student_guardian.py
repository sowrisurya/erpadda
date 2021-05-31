from __future__ import unicode_literals
import vmraid

def execute():
	if vmraid.db.exists("DocType", "Guardian"):

		# 'Schools' module changed to the 'Education'
		# vmraid.reload_doc("schools", "doctype", "student")
		# vmraid.reload_doc("schools", "doctype", "student_guardian")
		# vmraid.reload_doc("schools", "doctype", "student_sibling")

		vmraid.reload_doc("education", "doctype", "student")
		vmraid.reload_doc("education", "doctype", "student_guardian")
		vmraid.reload_doc("education", "doctype", "student_sibling")
		if "student" not in vmraid.db.get_table_columns("Guardian"):
			return
		guardian = vmraid.get_all("Guardian", fields=["name", "student"])
		for d in guardian:
			if d.student:
				student = vmraid.get_doc("Student", d.student)
				if student:
					student.append("guardians", {"guardian": d.name})
					student.save()
