# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("accounts", "doctype", "pricing_rule")
	vmraid.db.sql("""update `tabPricing Rule` set selling=1 where ifnull(applicable_for, '') in
		('', 'Customer', 'Customer Group', 'Territory', 'Sales Partner', 'Campaign')""")

	vmraid.db.sql("""update `tabPricing Rule` set buying=1 where ifnull(applicable_for, '') in
		('', 'Supplier', 'Supplier Type')""")
