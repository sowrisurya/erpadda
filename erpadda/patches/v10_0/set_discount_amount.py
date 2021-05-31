from __future__ import unicode_literals

import vmraid

def execute():
	vmraid.reload_doc("accounts", "doctype", "sales_invoice_item")
	vmraid.reload_doc('accounts', 'doctype', 'purchase_invoice_item')
	vmraid.reload_doc('buying', 'doctype', 'purchase_order_item')
	vmraid.reload_doc('buying', 'doctype', 'supplier_quotation_item')
	vmraid.reload_doc('selling', 'doctype', 'sales_order_item')
	vmraid.reload_doc('selling', 'doctype', 'quotation_item')
	vmraid.reload_doc('stock', 'doctype', 'delivery_note_item')
	vmraid.reload_doc('stock', 'doctype', 'purchase_receipt_item')

	selling_doctypes = ["Sales Order Item", "Sales Invoice Item", "Delivery Note Item", "Quotation Item"]
	buying_doctypes = ["Purchase Order Item", "Purchase Invoice Item", "Purchase Receipt Item", "Supplier Quotation Item"]

	for doctype in selling_doctypes:
		vmraid.db.sql('''
			UPDATE
				`tab%s`
			SET
				discount_amount = if(rate_with_margin > 0, rate_with_margin, price_list_rate) * discount_percentage / 100
			WHERE
				discount_percentage > 0
		''' % (doctype))
	for doctype in buying_doctypes:
		vmraid.db.sql('''
			UPDATE
				`tab%s`
			SET
				discount_amount = price_list_rate * discount_percentage / 100
			WHERE
				discount_percentage > 0
		''' % (doctype))