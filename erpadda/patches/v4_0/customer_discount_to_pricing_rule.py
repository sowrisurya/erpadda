# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.utils.nestedset import get_root_of

def execute():
	vmraid.reload_doc("accounts", "doctype", "pricing_rule")

	vmraid.db.auto_commit_on_many_writes = True

	default_item_group = get_root_of("Item Group")

	for d in vmraid.db.sql("""select * from `tabCustomer Discount`
		where ifnull(parent, '') != ''""", as_dict=1):
			if not d.discount:
				continue

			vmraid.get_doc({
				"doctype": "Pricing Rule",
				"apply_on": "Item Group",
				"item_group": d.item_group or default_item_group,
				"applicable_for": "Customer",
				"customer": d.parent,
				"price_or_discount": "Discount Percentage",
				"discount_percentage": d.discount,
				"selling": 1
			}).insert()

	vmraid.db.auto_commit_on_many_writes = False

	vmraid.delete_doc("DocType", "Customer Discount")
