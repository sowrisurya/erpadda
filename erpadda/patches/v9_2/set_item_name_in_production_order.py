from __future__ import unicode_literals
import vmraid

def execute():

	vmraid.db.sql("""
		update `tabBOM Item` bom, `tabWork Order Item` po_item
		set po_item.item_name = bom.item_name,
			po_item.description = bom.description
		where po_item.item_code = bom.item_code
			and (po_item.item_name is null or po_item.description is null)
	""")
