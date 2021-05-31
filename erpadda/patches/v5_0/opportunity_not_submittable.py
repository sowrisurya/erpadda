# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("Opportunity")
	vmraid.db.sql("update tabDocPerm set submit=0, cancel=0, amend=0 where parent='Opportunity'")
	vmraid.db.sql("update tabOpportunity set docstatus=0 where docstatus=1")
