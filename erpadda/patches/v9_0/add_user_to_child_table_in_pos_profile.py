# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	if vmraid.db.table_exists("POS Profile User"):
		vmraid.reload_doc('accounts', 'doctype', 'pos_profile_user')

		vmraid.db.sql(""" update `tabPOS Profile User`,
			(select `tabPOS Profile User`.name from `tabPOS Profile User`, `tabPOS Profile`
				where `tabPOS Profile`.name = `tabPOS Profile User`.parent
				group by `tabPOS Profile User`.user, `tabPOS Profile`.company) as pfu
			set
				`tabPOS Profile User`.default = 1
			where `tabPOS Profile User`.name = pfu.name""")
	else:
		doctype = 'POS Profile'
		vmraid.reload_doc('accounts', 'doctype', doctype)
		vmraid.reload_doc('accounts', 'doctype', 'pos_profile_user')
		vmraid.reload_doc('accounts', 'doctype', 'pos_item_group')
		vmraid.reload_doc('accounts', 'doctype', 'pos_customer_group')

		for doc in vmraid.get_all(doctype):
			_doc = vmraid.get_doc(doctype, doc.name)
			user = vmraid.db.get_value(doctype, doc.name, 'user')

			if not user: continue

			_doc.append('applicable_for_users', {
				'user': user,
				'default': 1
			})

			_doc.flags.ignore_validate  = True
			_doc.flags.ignore_mandatory = True
			_doc.save()