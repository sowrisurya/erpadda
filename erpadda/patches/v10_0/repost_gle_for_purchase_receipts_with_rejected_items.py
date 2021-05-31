# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid, erpadda

def execute():
	for company in vmraid.get_all("Company"):
		if not erpadda.is_perpetual_inventory_enabled(company.name):
			continue

		acc_frozen_upto = vmraid.db.get_value("Accounts Settings", None, "acc_frozen_upto") or "1900-01-01"
		pr_with_rejected_warehouse = vmraid.db.sql("""
			select pr.name
			from `tabPurchase Receipt` pr, `tabPurchase Receipt Item` pr_item
			where pr.name = pr_item.parent
				and pr.posting_date > %s
				and pr.docstatus=1
				and pr.company = %s
				and pr_item.rejected_qty > 0
		""", (acc_frozen_upto, company.name), as_dict=1)

		for d in pr_with_rejected_warehouse:
			doc = vmraid.get_doc("Purchase Receipt", d.name)

			doc.docstatus = 2
			doc.make_gl_entries_on_cancel()


			# update gl entries for submit state of PR
			doc.docstatus = 1
			doc.make_gl_entries()
