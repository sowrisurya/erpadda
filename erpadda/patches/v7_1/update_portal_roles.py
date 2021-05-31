from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype('Role')
	vmraid.reload_doctype('User')
	for role_name in ('Customer', 'Supplier', 'Student'):
		if vmraid.db.exists('Role', role_name):
			vmraid.db.set_value('Role', role_name, 'desk_access', 0)
		else:
			vmraid.get_doc(dict(doctype='Role', role_name=role_name, desk_access=0)).insert()


	# set customer, supplier roles
	for c in vmraid.get_all('Contact', fields=['user'], filters={'ifnull(user, "")': ('!=', '')}):
		user = vmraid.get_doc('User', c.user)
		user.flags.ignore_validate = True
		user.flags.ignore_mandatory = True
		user.save()


