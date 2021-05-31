# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("setup", 'doctype', "company")
	vmraid.reload_doc("accounts", 'doctype', "account")

	vmraid.db.sql("""update tabAccount set account_type='Cash'
		where account_type='Bank or Cash' and account_name in ('Cash', 'Cash In Hand')""")

	vmraid.db.sql("""update tabAccount set account_type='Stock'
		where account_name = 'Stock Assets'""")

	ac_types = {"Fixed Asset Account": "Fixed Asset", "Bank or Cash": "Bank"}
	for old, new in ac_types.items():
		vmraid.db.sql("""update tabAccount set account_type=%s
			where account_type=%s""", (new, old))

	try:
		vmraid.db.sql("""update `tabAccount` set report_type =
			if(is_pl_account='Yes', 'Profit and Loss', 'Balance Sheet')""")

		vmraid.db.sql("""update `tabAccount` set balance_must_be=debit_or_credit
			where ifnull(allow_negative_balance, 0) = 0""")
	except:
		pass
