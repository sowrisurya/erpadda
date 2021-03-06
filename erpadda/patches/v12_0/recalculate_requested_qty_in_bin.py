from __future__ import unicode_literals
import vmraid
from erpadda.stock.stock_balance import update_bin_qty, get_indented_qty

def execute():
	bin_details = vmraid.db.sql("""
		SELECT item_code, warehouse
		FROM `tabBin`""",as_dict=1)

	for entry in bin_details:
		update_bin_qty(entry.get("item_code"), entry.get("warehouse"), {
			"indented_qty": get_indented_qty(entry.get("item_code"), entry.get("warehouse"))
		})