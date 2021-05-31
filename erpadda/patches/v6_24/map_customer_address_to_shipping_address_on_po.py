# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("Purchase Order")
	
	if not vmraid.db.has_column("Purchase Order", "shipping_address"):
		return
		
	if not vmraid.db.has_column("Purchase Order", "customer_address"):
		return
	
	vmraid.db.sql("""update `tabPurchase Order` set shipping_address=customer_address, 
		shipping_address_display=customer_address_display""")
	
	vmraid.db.commit()