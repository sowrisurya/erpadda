from __future__ import unicode_literals
import vmraid

def execute():
	# remove missing lead
	for customer in vmraid.db.sql_list("""select name from `tabCustomer`
		where ifnull(lead_name, '')!='' and not exists (select name from `tabLead` where name=`tabCustomer`.lead_name)"""):
		vmraid.db.set_value("Customer", customer, "lead_name", None)

	# remove missing default taxes
	for customer in vmraid.db.sql_list("""select name from `tabCustomer`
		where ifnull(default_taxes_and_charges, '')!='' and not exists (
			select name from `tabSales Taxes and Charges Template` where name=`tabCustomer`.default_taxes_and_charges
		)"""):
		c = vmraid.get_doc("Customer", customer)
		c.default_taxes_and_charges = None
		c.save()

	for supplier in vmraid.db.sql_list("""select name from `tabSupplier`
		where ifnull(default_taxes_and_charges, '')!='' and not exists (
			select name from `tabPurchase Taxes and Charges Template` where name=`tabSupplier`.default_taxes_and_charges
		)"""):
		c = vmraid.get_doc("Supplier", supplier)
		c.default_taxes_and_charges = None
		c.save()
