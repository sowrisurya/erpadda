# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("POS Profile")
	vmraid.reload_doctype("Sales Invoice Payment")

	vmraid.db.sql("""
		update
			`tabSales Invoice Payment`
		set `tabSales Invoice Payment`.default = 1
		where
			`tabSales Invoice Payment`.parenttype = 'POS Profile'
			and `tabSales Invoice Payment`.idx=1""")