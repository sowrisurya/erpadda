# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	if not vmraid.db.get_value('DocPerm', {'parent': 'Timesheet', 'role': 'Accounts User', 'permlevel': 1}):
		doc = vmraid.get_doc('DocType', 'Timesheet')
		doc.append('permissions', {
			'role': "Accounts User",
			'permlevel': 0,
			'read': 1,
			'write': 1,
			'create': 1,
			'delete': 1,
			'submit': 1,
			'cancel': 1,
			'amend': 1,
			'report': 1,
			'email': 1
		})

		doc.append('permissions', {
			'role': "Accounts User",
			'permlevel': 1,
			'read': 1,
			'write': 1
		})

		doc.save(ignore_permissions=True)