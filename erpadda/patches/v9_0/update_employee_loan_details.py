# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('Payroll', 'doctype', 'salary_slip_loan')
	vmraid.reload_doc('Payroll', 'doctype', 'salary_slip')

	for data in vmraid.db.sql(""" select name,
			start_date, end_date, total_loan_repayment
		from
			`tabSalary Slip`
		where
			docstatus < 2 and ifnull(total_loan_repayment, 0) > 0""", as_dict=1):
		salary_slip = vmraid.get_doc('Salary Slip', data.name)
		salary_slip.set_loan_repayment()

		if salary_slip.total_loan_repayment == data.total_loan_repayment:
			for row in salary_slip.loans:
				row.db_update()

			salary_slip.db_update()
