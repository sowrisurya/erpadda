# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import vmraid

def execute():
	customers = vmraid._dict(vmraid.db.sql("select name, customer_name from tabCustomer"))
	suppliers = vmraid._dict(vmraid.db.sql("select name, supplier_name from tabSupplier"))
	
	vmraid.reload_doc('accounts', 'doctype', 'payment_entry')
	
	pe_list = vmraid.db.sql("""select name, party_type, party from `tabPayment Entry` 
		where party is not null and party != ''""", as_dict=1)
	for pe in pe_list:
		party_name = customers.get(pe.party) if pe.party_type=="Customer" else suppliers.get(pe.party)
		
		vmraid.db.set_value("Payment Entry", pe.name, "party_name", party_name, update_modified=False)
	
