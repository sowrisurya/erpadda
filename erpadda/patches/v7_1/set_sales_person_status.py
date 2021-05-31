from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('setup','doctype','sales_person')
	vmraid.db.sql("""update `tabSales Person` set enabled=1 
		where (employee is null or employee = '' 
			or employee IN (select employee from tabEmployee where status != "Left"))""")
