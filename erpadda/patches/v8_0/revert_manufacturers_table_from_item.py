# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	if vmraid.db.exists("DocType", "Item Manufacturer"):
		vmraid.reload_doctype("Item")
		item_manufacturers = vmraid.db.sql("""
			select parent, manufacturer, manufacturer_part_no 
			from `tabItem Manufacturer`
		""", as_dict=1)
		
		for im in item_manufacturers:
			vmraid.db.sql("""
				update tabItem 
				set manufacturer=%s, manufacturer_part_no=%s
				where name=%s
			""", (im.manufacturer, im.manufacturer_part_no, im.parent))
		
		vmraid.delete_doc("DocType", "Item Manufacturer")