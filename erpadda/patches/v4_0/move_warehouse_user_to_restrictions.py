# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
import vmraid.permissions

def execute():
	for warehouse, user in vmraid.db.sql("""select parent, user from `tabWarehouse User`"""):
		vmraid.permissions.add_user_permission("Warehouse", warehouse, user)

	vmraid.delete_doc_if_exists("DocType", "Warehouse User")
	vmraid.reload_doc("stock", "doctype", "warehouse")
