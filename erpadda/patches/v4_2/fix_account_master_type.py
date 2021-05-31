# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	for d in vmraid.db.sql("""select name from `tabAccount`
		where ifnull(master_type, '') not in ('Customer', 'Supplier', 'Employee', '') and docstatus=0"""):
			ac = vmraid.get_doc("Account", d[0])
			ac.master_type = None
			ac.save()
