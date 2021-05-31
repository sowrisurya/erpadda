# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("support", "doctype", "schedules")
	vmraid.reload_doc("support", "doctype", "maintenance_schedule_item")
	
	vmraid.db.sql("""update `tabMaintenance Schedule Detail` set sales_person=incharge_name""")
	vmraid.db.sql("""update `tabMaintenance Schedule Item` set sales_person=incharge_name""")