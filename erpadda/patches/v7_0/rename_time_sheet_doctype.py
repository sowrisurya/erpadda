from __future__ import unicode_literals
import vmraid

def execute():
	if vmraid.db.table_exists("Time Sheet") and not vmraid.db.table_exists("Timesheet"):
		vmraid.rename_doc("DocType", "Time Sheet", "Timesheet")
		vmraid.rename_doc("DocType", "Time Sheet Detail", "Timesheet Detail")
		
		for doctype in ['Time Sheet', 'Time Sheet Detail']:
			vmraid.delete_doc('DocType', doctype)
		
		report = "Daily Time Sheet Summary"
		if vmraid.db.exists("Report", report):
			vmraid.delete_doc('Report', report)
