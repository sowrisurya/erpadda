# Copyright (c) 2013, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("Time Log")
	for d in vmraid.get_all("Time Log"):
		time_log = vmraid.get_doc("Time Log", d.name)
		time_log.set_title()
		vmraid.db.set_value("Time Log", time_log.name, "title", time_log.title)
