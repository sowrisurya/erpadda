# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	if vmraid.db.exists("DocType", "Scheduling Tool"):
		vmraid.delete_doc("DocType", "Scheduling Tool", ignore_permissions=True)
