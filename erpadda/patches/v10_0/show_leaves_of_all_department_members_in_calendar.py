from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("hr", "doctype", "hr_settings")
	vmraid.db.set_value("HR Settings", None, "show_leaves_of_all_department_members_in_calendar", 1)