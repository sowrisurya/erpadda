from __future__ import unicode_literals
import vmraid
from vmraid.model.rename_doc import get_fetch_fields

def execute():
	ignore_doctypes = ["Lead", "Opportunity", "POS Profile", "Tax Rule", "Pricing Rule"]
	customers = vmraid.get_all('Customer', fields=["name", "customer_group"])
	customer_group_fetch = get_fetch_fields('Customer', 'Customer Group', ignore_doctypes)

	batch_size = 1000
	for i in range(0, len(customers), batch_size):
		batch_customers = customers[i:i + batch_size]
		for d in customer_group_fetch:
			when_then = []
			for customer in batch_customers:
				value = vmraid.db.escape(vmraid.as_unicode(customer.get("customer_group")))

				when_then.append('''
					WHEN `%s` = %s and %s != %s
					THEN %s
				'''%(d["master_fieldname"], vmraid.db.escape(vmraid.as_unicode(customer.name)),
					d["linked_to_fieldname"], value, value))

			vmraid.db.sql("""
				update
					`tab%s`
				set
					%s = CASE %s  ELSE `%s` END
			"""%(d['doctype'], d.linked_to_fieldname, " ".join(when_then), d.linked_to_fieldname))
