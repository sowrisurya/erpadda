from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("stock", "doctype", "purchase_receipt")
	vmraid.db.sql('''
		UPDATE `tabPurchase Receipt` SET status = "Completed" WHERE per_billed = 100 AND docstatus = 1
	''')