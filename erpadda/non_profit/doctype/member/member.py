# -*- coding: utf-8 -*-
# Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid import _
from vmraid.model.document import Document
from vmraid.contacts.address_and_contact import load_address_and_contact
from vmraid.utils import cint, get_link_to_form
from vmraid.integrations.utils import get_payment_gateway_controller
from erpadda.non_profit.doctype.membership_type.membership_type import get_membership_type

class Member(Document):
	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)


	def validate(self):
		if self.email_id:
			self.validate_email_type(self.email_id)

	def validate_email_type(self, email):
		from vmraid.utils import validate_email_address
		validate_email_address(email.strip(), True)

	def setup_subscription(self):
		non_profit_settings = vmraid.get_doc('Non Profit Settings')
		if not non_profit_settings.enable_razorpay_for_memberships:
			vmraid.throw('Please check Enable Razorpay for Memberships in {0} to setup subscription').format(
				get_link_to_form('Non Profit Settings', 'Non Profit Settings'))

		controller = get_payment_gateway_controller("Razorpay")
		settings = controller.get_settings({})

		plan_id = vmraid.get_value("Membership Type", self.membership_type, "razorpay_plan_id")

		if not plan_id:
			vmraid.throw(_("Please setup Razorpay Plan ID"))

		subscription_details = {
			"plan_id": plan_id,
			"billing_frequency": cint(non_profit_settings.billing_frequency),
			"customer_notify": 1
		}

		args = {
			'subscription_details': subscription_details
		}

		subscription = controller.setup_subscription(settings, **args)

		return subscription

	@vmraid.whitelist()
	def make_customer_and_link(self):
		if self.customer:
			vmraid.msgprint(_("A customer is already linked to this Member"))

		customer = create_customer(vmraid._dict({
			'fullname': self.member_name,
			'email': self.email_id,
			'phone': None
		}))

		self.customer = customer
		self.save()
		vmraid.msgprint(_("Customer {0} has been created succesfully.").format(self.customer))


def get_or_create_member(user_details):
	member_list = vmraid.get_all("Member", filters={'email': user_details.email, 'membership_type': user_details.plan_id})
	if member_list and member_list[0]:
		return member_list[0]['name']
	else:
		return create_member(user_details)

def create_member(user_details):
	user_details = vmraid._dict(user_details)
	member = vmraid.new_doc("Member")
	member.update({
		"member_name": user_details.fullname,
		"email_id": user_details.email,
		"pan_number": user_details.pan or None,
		"membership_type": user_details.plan_id,
		"subscription_id": user_details.subscription_id or None
	})

	member.insert(ignore_permissions=True)
	member.customer = create_customer(user_details, member.name)
	member.save(ignore_permissions=True)

	return member

def create_customer(user_details, member=None):
	customer = vmraid.new_doc("Customer")
	customer.customer_name = user_details.fullname
	customer.customer_type = "Individual"
	customer.flags.ignore_mandatory = True
	customer.insert(ignore_permissions=True)

	try:
		contact = vmraid.new_doc("Contact")
		contact.first_name = user_details.fullname
		if user_details.mobile:
			contact.add_phone(user_details.mobile, is_primary_phone=1, is_primary_mobile_no=1)
		if user_details.email:
			contact.add_email(user_details.email, is_primary=1)
		contact.insert(ignore_permissions=True)

		contact.append("links", {
			"link_doctype": "Customer",
			"link_name": customer.name
		})

		if member:
			contact.append("links", {
				"link_doctype": "Member",
				"link_name": member
			})

		contact.save(ignore_permissions=True)

	except vmraid.DuplicateEntryError:
		return customer.name

	except Exception as e:
		vmraid.log_error(vmraid.get_traceback(), _("Contact Creation Failed"))
		pass

	return customer.name

@vmraid.whitelist(allow_guest=True)
def create_member_subscription_order(user_details):
	"""Create Member subscription and order for payment

	Args:
		user_details (TYPE): Description

	Returns:
		Dictionary: Dictionary with subscription details
		{
			'subscription_details': {
										'plan_id': 'plan_EXwyxDYDCj3X4v',
										'billing_frequency': 24,
										'customer_notify': 1
									},
			'subscription_id': 'sub_EZycCvXFvqnC6p'
		}
	"""

	user_details = vmraid._dict(user_details)
	member = get_or_create_member(user_details)

	subscription = member.setup_subscription()

	member.subscription_id = subscription.get('subscription_id')
	member.save(ignore_permissions=True)

	return subscription

@vmraid.whitelist()
def register_member(fullname, email, rzpay_plan_id, subscription_id, pan=None, mobile=None):
	plan = get_membership_type(rzpay_plan_id)
	if not plan:
		raise vmraid.DoesNotExistError

	member = vmraid.db.exists("Member", {'email': email, 'subscription_id': subscription_id })
	if member:
		return member
	else:
		member = create_member(dict(
			fullname=fullname,
			email=email,
			plan_id=plan,
			subscription_id=subscription_id,
			pan=pan,
			mobile=mobile
		))

		return member.name
