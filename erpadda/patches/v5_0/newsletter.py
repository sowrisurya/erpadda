# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
import vmraid.permissions

def execute():
	vmraid.reload_doc("core", "doctype", "block_module")
	vmraid.reload_doctype("User")
	vmraid.reload_doctype("Lead")
	vmraid.reload_doctype("Contact")

	vmraid.reload_doc('email', 'doctype', 'email_group')
	vmraid.reload_doc('email', 'doctype', 'email_group_member')
	vmraid.reload_doc('email', 'doctype', 'newsletter')

	vmraid.permissions.reset_perms("Newsletter")

	if not vmraid.db.exists("Role", "Newsletter Manager"):
		vmraid.get_doc({"doctype": "Role", "role": "Newsletter Manager"}).insert()

	for userrole in vmraid.get_all("Has Role", "parent", {"role": "Sales Manager", "parenttype": "User"}):
		if vmraid.db.exists("User", userrole.parent):
			user = vmraid.get_doc("User", userrole.parent)
			user.append("roles", {
				"doctype": "Has Role",
				"role": "Newsletter Manager"
			})
			user.flags.ignore_mandatory = True
			user.save()

	# create default lists
	general = vmraid.new_doc("Email Group")
	general.title = "General"
	general.insert()
	general.import_from("Lead")
	general.import_from("Contact")
