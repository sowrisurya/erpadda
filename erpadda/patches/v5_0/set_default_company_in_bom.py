# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("manufacturing", "doctype", "bom")
	company = vmraid.db.get_value("Global Defaults", None, "default_company")
	vmraid.db.sql("""update  `tabBOM` set company = %s""",company)
