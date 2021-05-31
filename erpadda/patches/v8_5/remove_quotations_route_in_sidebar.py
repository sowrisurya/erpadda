# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("Portal Settings")

	vmraid.db.sql("""
		delete from
			`tabPortal Menu Item`
		where
			(route = '/quotations' and title = 'Supplier Quotation')
		or (route = '/quotation' and title = 'Quotations')
	""")