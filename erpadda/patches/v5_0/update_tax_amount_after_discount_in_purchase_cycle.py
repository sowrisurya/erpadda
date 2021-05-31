# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.db.sql("""
		update
			`tabPurchase Taxes and Charges`
		set
			tax_amount_after_discount_amount = tax_amount,
			base_tax_amount_after_discount_amount = base_tax_amount
		where
			ifnull(tax_amount_after_discount_amount, 0) = 0
			and ifnull(base_tax_amount_after_discount_amount, 0) = 0
	""")