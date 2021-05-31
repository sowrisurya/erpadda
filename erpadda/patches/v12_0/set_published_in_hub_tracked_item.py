from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("Hub Node", "doctype", "Hub Tracked Item")
	if not vmraid.db.a_row_exists("Hub Tracked Item"):
		return

	vmraid.db.sql('''
		Update `tabHub Tracked Item`
		SET published = 1
	''')
