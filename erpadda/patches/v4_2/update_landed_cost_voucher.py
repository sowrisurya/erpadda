# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("stock", "doctype", "landed_cost_voucher")
	vmraid.db.sql("""update `tabLanded Cost Voucher` set distribute_charges_based_on = 'Amount'
		where docstatus=1""")
