from __future__ import unicode_literals

import vmraid

def execute():
	vmraid.reload_doctype("Account")
	vmraid.reload_doctype("Cost Center")
	vmraid.db.sql("update tabAccount set is_group = if(group_or_ledger='Group', 1, 0)")
	vmraid.db.sql("update `tabCost Center` set is_group = if(group_or_ledger='Group', 1, 0)")
