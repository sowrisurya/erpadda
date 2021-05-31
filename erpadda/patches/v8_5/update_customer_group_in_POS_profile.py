from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype('POS Profile')
	customer_group = vmraid.db.get_single_value('Selling Settings', 'customer_group')
	if customer_group:
		vmraid.db.sql(""" update `tabPOS Profile`
			set customer_group = %s where customer_group is null """, (customer_group))