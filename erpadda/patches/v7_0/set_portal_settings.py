# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import vmraid

def execute():
	vmraid.reload_doctype('Role')
	for dt in ("assessment", "course", "fees"):
		# 'Schools' module changed to the 'Education'
		# vmraid.reload_doc("schools", "doctype", dt)
		vmraid.reload_doc("education", "doctype", dt)

	for dt in ("domain", "has_domain", "domain_settings"):
		vmraid.reload_doc("core", "doctype", dt)

	vmraid.reload_doc('website', 'doctype', 'portal_menu_item')

	vmraid.get_doc('Portal Settings').sync_menu()

	if 'schools' in vmraid.get_installed_apps():
		domain = vmraid.get_doc('Domain', 'Education')
		domain.setup_domain()
	else:
		domain = vmraid.get_doc('Domain', 'Manufacturing')
		domain.setup_data()
		domain.setup_sidebar_items()
