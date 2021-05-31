# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	old_formats = ("Sales Invoice", "Sales Invoice Spartan", "Sales Invoice Modern",
		"Sales Invoice Classic",
		"Sales Order Spartan", "Sales Order Modern", "Sales Order Classic",
		"Purchase Order Spartan", "Purchase Order Modern", "Purchase Order Classic",
		"Quotation Spartan", "Quotation Modern", "Quotation Classic",
		"Delivery Note Spartan", "Delivery Note Modern", "Delivery Note Classic")

	for fmt in old_formats:
		# update property setter
		for ps in vmraid.db.sql_list("""select name from `tabProperty Setter`
			where property='default_print_format' and value=%s""", fmt):
			ps = vmraid.get_doc("Property Setter", ps)
			ps.value = "Standard"
			ps.save(ignore_permissions = True)

		vmraid.delete_doc_if_exists("Print Format", fmt)
