# Copyright (c) 2020, VMRaid Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("accounts", "doctype", "Payment Schedule")
	if vmraid.db.count('Payment Schedule'):
		vmraid.db.sql('''
			UPDATE
				`tabPayment Schedule` ps
			SET
				ps.outstanding = (ps.payment_amount - ps.paid_amount)
		''')
