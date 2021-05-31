# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.db.sql("""update `tabSales Order` set delivery_status = 'Not Delivered'
		where delivery_status = 'Delivered' and ifnull(per_delivered, 0) = 0 and ifnull(docstatus, 0) in (0, 1)""")

	vmraid.db.sql("""update `tabSales Order` set billing_status = 'Not Billed'
		where billing_status = 'Billed' and ifnull(per_billed, 0) = 0 and ifnull(docstatus, 0) in (0, 1)""")
