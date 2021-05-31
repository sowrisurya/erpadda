# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from erpadda.stock.stock_balance import get_planned_qty, update_bin_qty

def execute():
	for item_code, warehouse in vmraid.db.sql("""select distinct production_item, fg_warehouse
		from `tabWork Order`"""):
			if vmraid.db.exists("Item", item_code) and vmraid.db.exists("Warehouse", warehouse):
				update_bin_qty(item_code, warehouse, {
					"planned_qty": get_planned_qty(item_code, warehouse)
				})
