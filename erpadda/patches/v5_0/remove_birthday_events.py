from __future__ import unicode_literals
import vmraid

def execute():
	for e in vmraid.db.sql_list("""select name from tabEvent where
		repeat_on='Every Year' and ref_type='Employee'"""):
		vmraid.delete_doc("Event", e, force=True)
