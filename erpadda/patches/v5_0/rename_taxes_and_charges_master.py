from __future__ import unicode_literals
import vmraid


def execute():
	if vmraid.db.table_exists("Sales Taxes and Charges Master"):
		vmraid.rename_doc("DocType", "Sales Taxes and Charges Master",
			"Sales Taxes and Charges Template")
		vmraid.delete_doc("DocType", "Sales Taxes and Charges Master")

	if vmraid.db.table_exists("Purchase Taxes and Charges Master"):
		vmraid.rename_doc("DocType", "Purchase Taxes and Charges Master",
			"Purchase Taxes and Charges Template")
		vmraid.delete_doc("DocType", "Purchase Taxes and Charges Master")
