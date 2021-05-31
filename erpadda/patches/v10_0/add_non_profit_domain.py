# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	domain = 'Non Profit'
	if not vmraid.db.exists('Domain', domain):
		vmraid.get_doc({
			'doctype': 'Domain',
			'domain': domain
		}).insert(ignore_permissions=True)

		vmraid.get_doc({
			'doctype': 'Role',
			'role_name': 'Non Profit Portal User',
			'desk_access': 0,
			'restrict_to_domain': domain
		}).insert(ignore_permissions=True)