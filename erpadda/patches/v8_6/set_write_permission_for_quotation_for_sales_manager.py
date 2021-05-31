# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	# Set write permission to permlevel 1 for sales manager role in Quotation doctype
	vmraid.db.sql(""" update `tabCustom DocPerm` set `tabCustom DocPerm`.write = 1
		where `tabCustom DocPerm`.parent = 'Quotation' and `tabCustom DocPerm`.role = 'Sales Manager'
		and `tabCustom DocPerm`.permlevel = 1 """)