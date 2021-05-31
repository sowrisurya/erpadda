from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("Email Digest")
	vmraid.db.sql("""update `tabEmail Digest` set expense_year_to_date =
		income_year_to_date""")

	if vmraid.db.exists("Email Digest", "Scheduler Errors"):
		vmraid.delete_doc("Email Digest", "Scheduler Errors")
