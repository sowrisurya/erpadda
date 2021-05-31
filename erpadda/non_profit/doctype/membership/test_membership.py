# -*- coding: utf-8 -*-
# Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals
import unittest
import vmraid
import erpadda
from erpadda.non_profit.doctype.member.member import create_member
from vmraid.utils import nowdate, add_months

class TestMembership(unittest.TestCase):
	def setUp(self):
		plan = setup_membership()

		# make test member
		self.member_doc = create_member(vmraid._dict({
				'fullname': "_Test_Member",
				'email': "_test_member_erpadda@example.com",
				'plan_id': plan.name
		}))
		self.member_doc.make_customer_and_link()
		self.member = self.member_doc.name

	def test_auto_generate_invoice_and_payment_entry(self):
		entry = make_membership(self.member)

		# Naive test to see if at all invoice was generated and attached to member
		# In any case if details were missing, the invoicing would throw an error
		invoice = entry.generate_invoice(save=True)
		self.assertEqual(invoice.name, entry.invoice)

	def test_renew_within_30_days(self):
		# create a membership for two months
		# Should work fine
		make_membership(self.member, { "from_date": nowdate() })
		make_membership(self.member, { "from_date": add_months(nowdate(), 1) })

		from vmraid.utils.user import add_role
		add_role("test@example.com", "Non Profit Manager")
		vmraid.set_user("test@example.com")

		# create next membership with expiry not within 30 days
		self.assertRaises(vmraid.ValidationError, make_membership, self.member, {
			"from_date": add_months(nowdate(), 2),
		})

		vmraid.set_user("Administrator")
		# create the same membership but as administrator
		make_membership(self.member, {
			"from_date": add_months(nowdate(), 2),
			"to_date": add_months(nowdate(), 3),
		})

def set_config(key, value):
	vmraid.db.set_value("Non Profit Settings", None, key, value)

def make_membership(member, payload={}):
	data = {
		"doctype": "Membership",
		"member": member,
		"membership_status": "Current",
		"membership_type": "_rzpy_test_milythm",
		"currency": "INR",
		"paid": 1,
		"from_date": nowdate(),
		"amount": 100
	}
	data.update(payload)
	membership = vmraid.get_doc(data)
	membership.insert(ignore_permissions=True, ignore_if_duplicate=True)
	return membership

def create_item(item_code):
	if not vmraid.db.exists("Item", item_code):
		item = vmraid.new_doc("Item")
		item.item_code = item_code
		item.item_name = item_code
		item.stock_uom = "Nos"
		item.description = item_code
		item.item_group = "All Item Groups"
		item.is_stock_item = 0
		item.save()
	else:
		item = vmraid.get_doc("Item", item_code)
	return item

def setup_membership():
	# Get default company
	company = vmraid.get_doc("Company", erpadda.get_default_company())

	# update non profit settings
	settings = vmraid.get_doc("Non Profit Settings")
	# Enable razorpay
	settings.enable_razorpay_for_memberships = 1
	settings.billing_cycle = "Monthly"
	settings.billing_frequency = 24
	# Enable invoicing
	settings.allow_invoicing = 1
	settings.automate_membership_payment_entries = 1
	settings.company = company.name
	settings.donation_company = company.name
	settings.membership_payment_account = company.default_cash_account
	settings.membership_debit_account = company.default_receivable_account
	settings.flags.ignore_mandatory = True
	settings.save()

	# make test plan
	if not vmraid.db.exists("Membership Type", "_rzpy_test_milythm"):
		plan = vmraid.new_doc("Membership Type")
		plan.membership_type = "_rzpy_test_milythm"
		plan.amount = 100
		plan.razorpay_plan_id = "_rzpy_test_milythm"
		plan.linked_item = create_item("_Test Item for Non Profit Membership").name
		plan.insert()
	else:
		plan = vmraid.get_doc("Membership Type", "_rzpy_test_milythm")

	return plan