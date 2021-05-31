from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype('Sales Order')
	vmraid.reload_doctype('Sales Invoice')
	vmraid.reload_doctype('Quotation')
	vmraid.reload_doctype('Delivery Note')

	doctype_list = ['Sales Order Item', 'Delivery Note Item', 'Quotation Item', 'Sales Invoice Item']

	for doctype in doctype_list:
		vmraid.reload_doctype(doctype)
		vmraid.db.sql("""update `tab{doctype}` 
		 		set uom = stock_uom, conversion_factor = 1, stock_qty = qty""".format(doctype=doctype))