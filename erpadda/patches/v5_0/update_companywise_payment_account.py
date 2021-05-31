# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('accounts', 'doctype', 'mode_of_payment')
	vmraid.reload_doc('accounts', 'doctype', 'mode_of_payment_account')

	mode_of_payment_list = vmraid.db.sql("""select name, default_account
		from `tabMode of Payment`""", as_dict=1)

	for d in mode_of_payment_list:
		if d.get("default_account"):
			parent_doc = vmraid.get_doc("Mode of Payment", d.get("name"))

			parent_doc.set("accounts",
				[{"company": vmraid.db.get_value("Account", d.get("default_account"), "company"),
				"default_account": d.get("default_account")}])
			parent_doc.save()
