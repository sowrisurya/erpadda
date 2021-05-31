# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('hr', 'doctype', 'employee')

	vmraid.db.sql("""
		UPDATE
			`tabEmployee`, `tabUser`
		SET
			`tabEmployee`.image = `tabUser`.user_image
		WHERE
			`tabEmployee`.user_id = `tabUser`.name and
			`tabEmployee`.user_id is not null and
			`tabEmployee`.user_id != '' and `tabEmployee`.image is null
	""")
