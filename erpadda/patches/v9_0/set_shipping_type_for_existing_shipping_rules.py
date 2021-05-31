# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("Shipping Rule")

	# default "calculate_based_on"
	vmraid.db.sql('''update `tabShipping Rule`
		set calculate_based_on = "Net Weight"
		where ifnull(calculate_based_on, '') = '' ''')

	# default "shipping_rule_type"
	vmraid.db.sql('''update `tabShipping Rule`
		set shipping_rule_type = "Selling"
		where ifnull(shipping_rule_type, '') = '' ''')
