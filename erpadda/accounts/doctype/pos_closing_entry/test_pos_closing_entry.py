# -*- coding: utf-8 -*-
# Copyright (c) 2018, VMRaid Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals
import vmraid
import unittest
from vmraid.utils import nowdate
from erpadda.stock.doctype.stock_entry.test_stock_entry import make_stock_entry
from erpadda.accounts.doctype.pos_invoice.test_pos_invoice import create_pos_invoice
from erpadda.accounts.doctype.pos_closing_entry.pos_closing_entry import make_closing_entry_from_opening
from erpadda.accounts.doctype.pos_opening_entry.test_pos_opening_entry import create_opening_entry
from erpadda.accounts.doctype.pos_profile.test_pos_profile import make_pos_profile

class TestPOSClosingEntry(unittest.TestCase):
	def setUp(self):
		# Make stock available for POS Sales
		make_stock_entry(target="_Test Warehouse - _TC", qty=2, basic_rate=100)

	def tearDown(self):
		vmraid.set_user("Administrator")
		vmraid.db.sql("delete from `tabPOS Profile`")

	def test_pos_closing_entry(self):
		test_user, pos_profile = init_user_and_profile()
		opening_entry = create_opening_entry(pos_profile, test_user.name)

		pos_inv1 = create_pos_invoice(rate=3500, do_not_submit=1)
		pos_inv1.append('payments', {
			'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3500
		})
		pos_inv1.submit()

		pos_inv2 = create_pos_invoice(rate=3200, do_not_submit=1)
		pos_inv2.append('payments', {
			'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3200
		})
		pos_inv2.submit()

		pcv_doc = make_closing_entry_from_opening(opening_entry)
		payment = pcv_doc.payment_reconciliation[0]

		self.assertEqual(payment.mode_of_payment, 'Cash')

		for d in pcv_doc.payment_reconciliation:
			if d.mode_of_payment == 'Cash':
				d.closing_amount = 6700

		pcv_doc.submit()

		self.assertEqual(pcv_doc.total_quantity, 2)
		self.assertEqual(pcv_doc.net_total, 6700)

	def test_cancelling_of_pos_closing_entry(self):
		test_user, pos_profile = init_user_and_profile()
		opening_entry = create_opening_entry(pos_profile, test_user.name)

		pos_inv1 = create_pos_invoice(rate=3500, do_not_submit=1)
		pos_inv1.append('payments', {
			'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3500
		})
		pos_inv1.submit()

		pos_inv2 = create_pos_invoice(rate=3200, do_not_submit=1)
		pos_inv2.append('payments', {
			'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3200
		})
		pos_inv2.submit()

		pcv_doc = make_closing_entry_from_opening(opening_entry)
		payment = pcv_doc.payment_reconciliation[0]

		self.assertEqual(payment.mode_of_payment, 'Cash')

		for d in pcv_doc.payment_reconciliation:
			if d.mode_of_payment == 'Cash':
				d.closing_amount = 6700

		pcv_doc.submit()

		pos_inv1.load_from_db()
		self.assertRaises(vmraid.ValidationError, pos_inv1.cancel)

		si_doc = vmraid.get_doc("Sales Invoice", pos_inv1.consolidated_invoice)
		self.assertRaises(vmraid.ValidationError, si_doc.cancel)

		pcv_doc.load_from_db()
		pcv_doc.cancel()
		si_doc.load_from_db()
		pos_inv1.load_from_db()
		self.assertEqual(si_doc.docstatus, 2)
		self.assertEqual(pos_inv1.status, 'Paid')


def init_user_and_profile(**args):
	user = 'test@example.com'
	test_user = vmraid.get_doc('User', user)

	roles = ("Accounts Manager", "Accounts User", "Sales Manager")
	test_user.add_roles(*roles)
	vmraid.set_user(user)

	pos_profile = make_pos_profile(**args)
	pos_profile.append('applicable_for_users', {
		'default': 1,
		'user': user
	})

	pos_profile.save()

	return test_user, pos_profile