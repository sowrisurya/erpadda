# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype('Timesheet')
	company = vmraid.get_all('Company')

	#Check more than one company exists
	if len(company) > 1:
		vmraid.db.sql(""" update `tabTimesheet` set `tabTimesheet`.company =
			(select company from `tabWork Order` where name = `tabTimesheet`.work_order)
			where workn_order is not null and work_order !=''""")