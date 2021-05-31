# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	# create guardian role
	if not vmraid.get_value('Role', dict(role_name='Guardian')):
		vmraid.get_doc({
			'doctype': 'Role',
			'role_name': 'Guardian',
			'desk_access': 0,
			'restrict_to_domain': 'Education'
		}).insert(ignore_permissions=True)
	
	# set guardian roles in already created users
	if vmraid.db.exists("Doctype", "Guardian"):
		for user in vmraid.db.sql_list("""select u.name from `tabUser` u , `tabGuardian` g where g.email_address = u.name"""):
			user = vmraid.get_doc('User', user)
			user.flags.ignore_validate = True
			user.flags.ignore_mandatory = True
			user.save()
