from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("accounts", "doctype", "account")
	
	vmraid.db.sql(""" update tabAccount set account_type = "Stock"
		where account_type = "Warehouse" """)
	
	vmraid.db.commit()