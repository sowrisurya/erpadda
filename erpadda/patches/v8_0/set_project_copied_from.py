from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("Project")
	
	vmraid.db.sql('''
		UPDATE `tabProject`
		SET copied_from=name
		WHERE copied_from is NULL
	''')