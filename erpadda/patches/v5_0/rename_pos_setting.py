from __future__ import unicode_literals
import vmraid

def execute():
	if vmraid.db.table_exists("POS Setting"):
		vmraid.rename_doc("DocType", "POS Setting", "POS Profile")
