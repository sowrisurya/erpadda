# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("Warehouse")
	vmraid.db.sql("""
		update 
			`tabWarehouse` 
		set 
			account = (select name from `tabAccount` 
				where account_type = 'Stock' and 
				warehouse = `tabWarehouse`.name and is_group = 0 limit 1)""")