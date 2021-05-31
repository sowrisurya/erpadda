from __future__ import unicode_literals
import vmraid

def execute():
	for doctype, fieldname in (
		("Sales Order", "per_billed"),
		("Sales Order", "per_delivered"),
		("Delivery Note", "per_installed"),
		("Purchase Order", "per_billed"),
		("Purchase Order", "per_received"),
		("Material Request", "per_ordered"),
	):
		vmraid.db.sql("""update `tab{doctype}` set `{fieldname}`=round(`{fieldname}`, 2)""".format(
			doctype=doctype, fieldname=fieldname))
