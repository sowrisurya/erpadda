# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype('Sales Invoice')

	vmraid.db.sql("""
		delete from 
			`tabSales Invoice Payment` 
		where 
			parent in (select name from `tabSales Invoice` where is_pos = 0)
	""")