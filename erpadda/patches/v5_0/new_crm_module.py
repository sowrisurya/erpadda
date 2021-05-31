# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import json
import vmraid

def execute():
	vmraid.reload_doc('crm', 'doctype', 'lead')
	vmraid.reload_doc('crm', 'doctype', 'opportunity')

	add_crm_to_user_desktop_items()

def add_crm_to_user_desktop_items():
	key = "_user_desktop_items"
	for user in vmraid.get_all("User", filters={"enabled": 1, "user_type": "System User"}):
		user = user.name
		user_desktop_items = vmraid.db.get_defaults(key, parent=user)
		if user_desktop_items:
			user_desktop_items = json.loads(user_desktop_items)
			if "CRM" not in user_desktop_items:
				user_desktop_items.append("CRM")
				vmraid.db.set_default(key, json.dumps(user_desktop_items), parent=user)

