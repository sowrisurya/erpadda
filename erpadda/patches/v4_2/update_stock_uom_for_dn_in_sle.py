# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.db.sql("""update `tabStock Ledger Entry` sle, tabItem item
		set sle.stock_uom = item.stock_uom
		where sle.voucher_type="Delivery Note" and item.name = sle.item_code
		and sle.stock_uom != item.stock_uom""")
