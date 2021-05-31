from __future__ import unicode_literals
import vmraid

def execute():
	try:
		vmraid.db.sql("UPDATE `tabStock Ledger Entry` SET is_cancelled = 0 where is_cancelled in ('', NULL, 'No')")
		vmraid.db.sql("UPDATE `tabSerial No` SET is_cancelled = 0 where is_cancelled in ('', NULL, 'No')")

		vmraid.db.sql("UPDATE `tabStock Ledger Entry` SET is_cancelled = 1 where is_cancelled = 'Yes'")
		vmraid.db.sql("UPDATE `tabSerial No` SET is_cancelled = 1 where is_cancelled = 'Yes'")

		vmraid.reload_doc("stock", "doctype", "stock_ledger_entry")
		vmraid.reload_doc("stock", "doctype", "serial_no")
	except:
		pass