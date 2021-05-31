from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("Quotation")
	vmraid.db.sql("""update tabQuotation set title = customer_name""")

	vmraid.reload_doctype("Sales Order")
	vmraid.db.sql("""update `tabSales Order` set title = customer_name""")

	vmraid.reload_doctype("Delivery Note")
	vmraid.db.sql("""update `tabDelivery Note` set title = customer_name""")

	vmraid.reload_doctype("Material Request")
	vmraid.db.sql("""update `tabMaterial Request` set title = material_request_type""")

	vmraid.reload_doctype("Supplier Quotation")
	vmraid.db.sql("""update `tabSupplier Quotation` set title = supplier_name""")

	vmraid.reload_doctype("Purchase Order")
	vmraid.db.sql("""update `tabPurchase Order` set title = supplier_name""")

	vmraid.reload_doctype("Purchase Receipt")
	vmraid.db.sql("""update `tabPurchase Receipt` set title = supplier_name""")

	vmraid.reload_doctype("Purchase Invoice")
	vmraid.db.sql("""update `tabPurchase Invoice` set title = supplier_name""")

	vmraid.reload_doctype("Stock Entry")
	vmraid.db.sql("""update `tabStock Entry` set title = purpose""")

	vmraid.reload_doctype("Sales Invoice")
	vmraid.db.sql("""update `tabSales Invoice` set title = customer_name""")

	vmraid.reload_doctype("Expense Claim")
	vmraid.db.sql("""update `tabExpense Claim` set title = employee_name""")
