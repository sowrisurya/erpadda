# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("stock", "doctype", "stock_settings")

	ss = vmraid.get_doc("Stock Settings")
	ss.set_qty_in_transactions_based_on_serial_no_input = 1

	if ss.default_warehouse \
		and not vmraid.db.exists("Warehouse", ss.default_warehouse):
			ss.default_warehouse = None

	if ss.stock_uom and not vmraid.db.exists("UOM", ss.stock_uom):
		ss.stock_uom = None

	ss.flags.ignore_mandatory = True
	ss.save()