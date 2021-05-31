# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("manufacturing", "doctype", "bom")
	vmraid.reload_doc("manufacturing", "doctype", "bom_item")
	vmraid.reload_doc("manufacturing", "doctype", "bom_explosion_item")
	vmraid.reload_doc("manufacturing", "doctype", "bom_operation")

	vmraid.db.sql("""update `tabBOM` as bom  set bom.item_name = \
		( select item.item_name from `tabItem` as item  where item.name = bom.item)""")
	vmraid.db.sql("""update `tabBOM Item` as bomItem set bomItem.item_name = ( select item.item_name  \
		from `tabItem` as item where item.name = bomItem.item_code)""")
	vmraid.db.sql("""update `tabBOM Explosion Item` as explosionItem set explosionItem.item_name = \
		( select item.item_name from `tabItem` as item where item.name = explosionItem.item_code)""")
