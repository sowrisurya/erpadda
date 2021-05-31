from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("accounts", "doctype", "budget")
	vmraid.db.sql("""
		update
			`tabBudget`
		set
			budget_against = 'Cost Center'
		""")
