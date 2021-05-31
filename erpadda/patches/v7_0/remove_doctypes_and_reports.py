from __future__ import unicode_literals
import vmraid

def execute():
	if vmraid.db.table_exists("Time Log"):
		vmraid.db.sql("""delete from `tabDocType`
			where name in('Time Log Batch', 'Time Log Batch Detail', 'Time Log')""")

	vmraid.db.sql("""delete from `tabDocField` where parent in ('Time Log', 'Time Log Batch')""")
	vmraid.db.sql("""update `tabClient Script` set dt = 'Timesheet' where dt = 'Time Log'""")

	for data in vmraid.db.sql(""" select label, fieldname from  `tabCustom Field` where dt = 'Time Log'""", as_dict=1):
		custom_field = vmraid.get_doc({
			'doctype': 'Custom Field',
			'label': data.label,
			'dt': 'Timesheet Detail',
			'fieldname': data.fieldname,
			'fieldtype': data.fieldtype or "Data"
		}).insert(ignore_permissions=True)

	vmraid.db.sql("""delete from `tabCustom Field` where dt = 'Time Log'""")
	vmraid.reload_doc('projects', 'doctype', 'timesheet')
	vmraid.reload_doc('projects', 'doctype', 'timesheet_detail')

	report = "Daily Time Log Summary"
	if vmraid.db.exists("Report", report):
		vmraid.delete_doc('Report', report)
