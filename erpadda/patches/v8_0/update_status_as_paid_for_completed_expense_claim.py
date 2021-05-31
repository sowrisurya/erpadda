# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	""" set status as Paid in Expense Claim if total_sactioned_amount 
		and total_amount_reimbursed is equal """
	
	vmraid.reload_doctype('Expense Claim')

	vmraid.db.sql("""
		update 
			`tabExpense Claim`
		set status = 'Paid'
		where 
			total_sanctioned_amount = total_amount_reimbursed
	""")
