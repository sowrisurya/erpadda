from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.db.sql("""update `tabStock Entry` set purpose='Material Transfer for Manufacture'
		where ifnull(work_order, '')!='' and purpose='Material Transfer'""")
