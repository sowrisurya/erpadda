# -*- coding: utf-8 -*-
# Copyright (c) 2021, VMRaid Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import vmraid
import unittest
from vmraid.utils import getdate
from erpadda.accounts.utils import get_fiscal_year
from erpadda.non_profit.doctype.donation.test_donation import create_donor, create_mode_of_payment, create_donor_type
from erpadda.non_profit.doctype.donation.donation import create_donation
from erpadda.non_profit.doctype.membership.test_membership import setup_membership, make_membership
from erpadda.non_profit.doctype.member.member import create_member

class TestTaxExemption80GCertificate(unittest.TestCase):
	def setUp(self):
		vmraid.db.sql('delete from `tabTax Exemption 80G Certificate`')
		vmraid.db.sql('delete from `tabMembership`')
		create_donor_type()
		settings = vmraid.get_doc('Non Profit Settings')
		settings.company = '_Test Company'
		settings.donation_company = '_Test Company'
		settings.default_donor_type = '_Test Donor'
		settings.creation_user = 'Administrator'
		settings.save()

		company = vmraid.get_doc('Company', '_Test Company')
		company.pan_details = 'BBBTI3374C'
		company.company_80g_number = 'NQ.CIT(E)I2018-19/DEL-IE28615-27062018/10087'
		company.with_effect_from = getdate()
		company.save()

	def test_duplicate_donation_certificate(self):
		donor = create_donor()
		create_mode_of_payment()
		payment = vmraid._dict({
			'amount': 100,
			'method': 'Debit Card',
			'id': 'pay_MeXAmsgeKOhq7O'
		})
		donation = create_donation(donor, payment)

		args = vmraid._dict({
			'recipient': 'Donor',
			'donor': donor.name,
			'donation': donation.name
		})
		certificate = create_80g_certificate(args)
		certificate.insert()

		# check company details
		self.assertEqual(certificate.company_pan_number, 'BBBTI3374C')
		self.assertEqual(certificate.company_80g_number, 'NQ.CIT(E)I2018-19/DEL-IE28615-27062018/10087')

		# check donation details
		self.assertEqual(certificate.amount, donation.amount)

		duplicate_certificate = create_80g_certificate(args)
		# duplicate validation
		self.assertRaises(vmraid.ValidationError, duplicate_certificate.insert)

	def test_membership_80g_certificate(self):
		plan = setup_membership()

		# make test member
		member_doc = create_member(vmraid._dict({
			'fullname': "_Test_Member",
			'email': "_test_member_erpadda@example.com",
			'plan_id': plan.name
		}))
		member_doc.make_customer_and_link()
		member = member_doc.name

		membership = make_membership(member, { "from_date": getdate() })
		invoice = membership.generate_invoice(save=True)

		args = vmraid._dict({
			'recipient': 'Member',
			'member': member,
			'fiscal_year': get_fiscal_year(getdate(), as_dict=True).get('name')
		})
		certificate = create_80g_certificate(args)
		certificate.get_payments()
		certificate.insert()

		self.assertEqual(len(certificate.payments), 1)
		self.assertEqual(certificate.payments[0].amount, membership.amount)
		self.assertEqual(certificate.payments[0].invoice_id, invoice.name)


def create_80g_certificate(args):
	certificate = vmraid.get_doc({
		'doctype': 'Tax Exemption 80G Certificate',
		'recipient': args.recipient,
		'date': getdate(),
		'company': '_Test Company'
	})

	certificate.update(args)

	return certificate