from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype('Supplier Quotation Item')
	for data in vmraid.db.sql(""" select prevdoc_docname, prevdoc_detail_docname, name
		from `tabSupplier Quotation Item` where prevdoc_docname is not null""", as_dict=True):
		vmraid.db.set_value("Supplier Quotation Item", data.name, "material_request", data.prevdoc_docname)
		vmraid.db.set_value("Supplier Quotation Item", data.name, "material_request_item", data.prevdoc_detail_docname)