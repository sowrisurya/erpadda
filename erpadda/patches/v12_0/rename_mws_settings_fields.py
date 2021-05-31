# Copyright (c) 2020, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

import vmraid

def execute():
	count = vmraid.db.sql("SELECT COUNT(*) FROM `tabSingles` WHERE doctype='Amazon MWS Settings' AND field='enable_sync';")[0][0]
	if count == 0:
		vmraid.db.sql("UPDATE `tabSingles` SET field='enable_sync' WHERE doctype='Amazon MWS Settings' AND field='enable_synch';")

	vmraid.reload_doc("ERPAdda Integrations", "doctype", "Amazon MWS Settings")
