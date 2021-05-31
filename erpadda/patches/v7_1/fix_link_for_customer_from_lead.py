from __future__ import unicode_literals
import vmraid

def execute():
	for c in vmraid.db.sql('select name from tabCustomer where ifnull(lead_name,"")!=""'):
		customer = vmraid.get_doc('Customer', c[0])
		customer.update_lead_status()