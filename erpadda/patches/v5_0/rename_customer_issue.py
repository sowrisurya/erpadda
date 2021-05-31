from __future__ import unicode_literals
import vmraid

def execute():
	if vmraid.db.table_exists("Customer Issue"):
		vmraid.rename_doc("DocType", "Customer Issue", "Warranty Claim")
