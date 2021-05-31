from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("stock", "doctype", "price_list_country")
	vmraid.reload_doc("accounts", "doctype", "shipping_rule_country")
	vmraid.reload_doctype("Price List")
	vmraid.reload_doctype("Shipping Rule")
	vmraid.reload_doctype("shopping_cart", "doctype", "shopping_cart_settings")

	# for price list
	countries = vmraid.db.sql_list("select name from tabCountry")

	for doctype in ("Price List", "Shipping Rule"):
		for at in vmraid.db.sql("""select name, parent, territory from `tabApplicable Territory` where
			parenttype = %s """, doctype, as_dict=True):
			if at.territory in countries:
				parent = vmraid.get_doc(doctype, at.parent)
				if not parent.countries:
					parent.append("countries", {"country": at.territory})
				parent.save()


	vmraid.delete_doc("DocType", "Applicable Territory")
