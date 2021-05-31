# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype('Expense Claim')

	for data in vmraid.db.sql(""" select name from `tabExpense Claim`
		where (docstatus=1 and total_sanctioned_amount=0 and status = 'Paid') or 
		(docstatus = 1 and approval_status = 'Rejected' and total_sanctioned_amount > 0)""", as_dict=1):
		doc = vmraid.get_doc('Expense Claim', data.name)
		if doc.approval_status == 'Rejected':
			for d in doc.expenses:
				d.db_set("sanctioned_amount", 0, update_modified = False)
			doc.db_set("total_sanctioned_amount", 0, update_modified = False)

			vmraid.db.sql(""" delete from `tabGL Entry` where voucher_type = 'Expense Claim'
				and voucher_no = %s""", (doc.name))

		doc.set_status()
		doc.db_set("status", doc.status, update_modified = False)