# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('manufacturing', 'doctype', 'bom_item')
	vmraid.reload_doc('manufacturing', 'doctype', 'bom_explosion_item')
	vmraid.reload_doc('manufacturing', 'doctype', 'bom_scrap_item')
	vmraid.db.sql("update `tabBOM Item` set stock_qty = qty, uom = stock_uom, conversion_factor = 1")
	vmraid.db.sql("update `tabBOM Explosion Item` set stock_qty = qty")
	if "qty" in vmraid.db.get_table_columns("BOM Scrap Item"):
		vmraid.db.sql("update `tabBOM Scrap Item` set stock_qty = qty")