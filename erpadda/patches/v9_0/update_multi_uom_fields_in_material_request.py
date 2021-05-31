# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype('Material Request')
	vmraid.reload_doctype('Material Request Item')

	vmraid.db.sql(""" update `tabMaterial Request Item`
		set stock_uom = uom, stock_qty = qty, conversion_factor = 1.0""")