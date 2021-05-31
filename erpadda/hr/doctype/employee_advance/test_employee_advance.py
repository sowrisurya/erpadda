# -*- coding: utf-8 -*-
# Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import vmraid, erpadda
import unittest
from vmraid.utils import nowdate
from erpadda.hr.doctype.employee_advance.employee_advance import make_bank_entry
from erpadda.hr.doctype.employee_advance.employee_advance import EmployeeAdvanceOverPayment
from erpadda.hr.doctype.employee.test_employee import make_employee

class TestEmployeeAdvance(unittest.TestCase):
	def test_paid_amount_and_status(self):
		employee_name = make_employee("_T@employe.advance")
		advance = make_employee_advance(employee_name)

		journal_entry = make_payment_entry(advance)
		journal_entry.submit()

		advance.reload()

		self.assertEqual(advance.paid_amount, 1000)
		self.assertEqual(advance.status, "Paid")

		# try making over payment
		journal_entry1 = make_payment_entry(advance)
		self.assertRaises(EmployeeAdvanceOverPayment, journal_entry1.submit)

def make_payment_entry(advance):
	journal_entry = vmraid.get_doc(make_bank_entry("Employee Advance", advance.name))
	journal_entry.cheque_no = "123123"
	journal_entry.cheque_date = nowdate()
	journal_entry.save()

	return journal_entry

def make_employee_advance(employee_name):
	doc = vmraid.new_doc("Employee Advance")
	doc.employee = employee_name
	doc.company  = "_Test company"
	doc.purpose = "For site visit"
	doc.currency = erpadda.get_company_currency("_Test company")
	doc.exchange_rate = 1
	doc.advance_amount = 1000
	doc.posting_date = nowdate()
	doc.advance_account = "_Test Employee Advance - _TC"
	doc.insert()
	doc.submit()

	return doc