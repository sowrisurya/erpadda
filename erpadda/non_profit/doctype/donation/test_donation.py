# -*- coding: utf-8 -*-
# Copyright (c) 2021, VMRaid Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import vmraid
import unittest
from erpadda.non_profit.doctype.donation.donation import create_donation

class TestDonation(unittest.TestCase):
	def setUp(self):
		create_donor_type()
		settings = vmraid.get_doc('Non Profit Settings')
		settings.company = '_Test Company'
		settings.donation_company = '_Test Company'
		settings.default_donor_type = '_Test Donor'
		settings.automate_donation_payment_entries = 1
		settings.donation_debit_account = 'Debtors - _TC'
		settings.donation_payment_account =  'Cash - _TC'
		settings.creation_user = 'Administrator'
		settings.flags.ignore_permissions = True
		settings.save()

	def test_payment_entry_for_donations(self):
		donor = create_donor()
		create_mode_of_payment()
		payment = vmraid._dict({
			'amount': 100,
			'method': 'Debit Card',
			'id': 'pay_MeXAmsgeKOhq7O'
		})
		donation = create_donation(donor, payment)

		self.assertTrue(donation.name)

		# Naive test to check if at all payment entry is generated
		# This method is actually triggered from Payment Gateway
		# In any case if details were missing, this would throw an error
		donation.on_payment_authorized()
		donation.reload()

		self.assertEqual(donation.paid, 1)
		self.assertTrue(vmraid.db.exists('Payment Entry', {'reference_no': donation.name}))


def create_donor_type():
	if not vmraid.db.exists('Donor Type', '_Test Donor'):
		vmraid.get_doc({
			'doctype': 'Donor Type',
			'donor_type': '_Test Donor'
		}).insert()


def create_donor():
	donor = vmraid.db.exists('Donor', 'donor@test.com')
	if donor:
		return vmraid.get_doc('Donor', 'donor@test.com')
	else:
		return vmraid.get_doc({
			'doctype': 'Donor',
			'donor_name': '_Test Donor',
			'donor_type': '_Test Donor',
			'email': 'donor@test.com'
		}).insert()


def create_mode_of_payment():
	if not vmraid.db.exists('Mode of Payment', 'Debit Card'):
		vmraid.get_doc({
			'doctype': 'Mode of Payment',
			'mode_of_payment': 'Debit Card',
			'accounts': [{
				'company': '_Test Company',
				'default_account': 'Cash - _TC'
			}]
		}).insert()