# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	domain = 'Agriculture'
	if not vmraid.db.exists('Domain', domain):
		vmraid.get_doc({
			'doctype': 'Domain',
			'domain': domain
		}).insert(ignore_permissions=True)