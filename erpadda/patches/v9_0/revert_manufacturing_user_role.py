from __future__ import unicode_literals
import vmraid

def execute():
	if 'Manufacturing' in vmraid.get_active_domains(): return

	role = 'Manufacturing User'
	vmraid.db.set_value('Role', role, 'restrict_to_domain', '')
	vmraid.db.set_value('Role', role, 'disabled', 0)

	users = vmraid.get_all('Has Role', filters = {
		'parenttype': 'User',
		'role': ('in', ['System Manager', 'Manufacturing Manager'])
	}, fields=['parent'], as_list=1)

	for user in users:
		_user = vmraid.get_doc('User', user[0])
		_user.append('roles', {
			'role': role
		})
		_user.flags.ignore_validate = True
		_user.save()
