# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("accounts", "doctype", "tax_rule")

	customers = vmraid.db.sql("""select name, default_taxes_and_charges from tabCustomer where
		ifnull(default_taxes_and_charges, '') != '' """, as_dict=1)

	for d in customers:
		if not vmraid.db.sql("select name from `tabTax Rule` where customer=%s", d.name):
			tr = vmraid.new_doc("Tax Rule")
			tr.tax_type = "Sales"
			tr.customer = d.name
			tr.sales_tax_template = d.default_taxes_and_charges
			tr.save()


	suppliers = vmraid.db.sql("""select name, default_taxes_and_charges from tabSupplier where
		ifnull(default_taxes_and_charges, '') != '' """, as_dict=1)

	for d in suppliers:
		if not vmraid.db.sql("select name from `tabTax Rule` where supplier=%s", d.name):
			tr = vmraid.new_doc("Tax Rule")
			tr.tax_type = "Purchase"
			tr.supplier = d.name
			tr.purchase_tax_template = d.default_taxes_and_charges
			tr.save()