# -*- coding: utf-8 -*-
# Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import json
import vmraid
import six
import os
from datetime import datetime
from vmraid.model.document import Document
from vmraid.email import sendmail_to_system_managers
from vmraid.utils import add_days, add_years, nowdate, getdate, add_months, get_link_to_form
from erpadda.non_profit.doctype.member.member import create_member
from vmraid import _
import erpadda

class Membership(Document):
	def validate(self):
		if not self.member or not vmraid.db.exists("Member", self.member):
			# for web forms
			user_type = vmraid.db.get_value("User", vmraid.session.user, "user_type")
			if user_type == "Website User":
				self.create_member_from_website_user()
			else:
				vmraid.throw(_("Please select a Member"))

		self.validate_membership_period()

	def create_member_from_website_user(self):
		member_name = vmraid.get_value("Member", dict(email_id=vmraid.session.user))

		if not member_name:
			user = vmraid.get_doc("User", vmraid.session.user)
			member = vmraid.get_doc(dict(
				doctype="Member",
				email_id=vmraid.session.user,
				membership_type=self.membership_type,
				member_name=user.get_fullname()
			)).insert(ignore_permissions=True)
			member_name = member.name

		if self.get("__islocal"):
			self.member = member_name

	def validate_membership_period(self):
		# get last membership (if active)
		last_membership = erpadda.get_last_membership(self.member)

		# if person applied for offline membership
		if last_membership and last_membership.name != self.name and not vmraid.session.user == "Administrator":
			# if last membership does not expire in 30 days, then do not allow to renew
			if getdate(add_days(last_membership.to_date, -30)) > getdate(nowdate()) :
				vmraid.throw(_("You can only renew if your membership expires within 30 days"))

			self.from_date = add_days(last_membership.to_date, 1)
		elif vmraid.session.user == "Administrator":
			self.from_date = self.from_date
		else:
			self.from_date = nowdate()

		if vmraid.db.get_single_value("Non Profit Settings", "billing_cycle") == "Yearly":
			self.to_date = add_years(self.from_date, 1)
		else:
			self.to_date = add_months(self.from_date, 1)

	def on_payment_authorized(self, status_changed_to=None):
		if status_changed_to not in ("Completed", "Authorized"):
			return
		self.load_from_db()
		self.db_set("paid", 1)
		settings = vmraid.get_doc("Non Profit Settings")
		if settings.allow_invoicing and settings.automate_membership_invoicing:
			self.generate_invoice(with_payment_entry=settings.automate_membership_payment_entries, save=True)


	@vmraid.whitelist()
	def generate_invoice(self, save=True, with_payment_entry=False):
		if not (self.paid or self.currency or self.amount):
			vmraid.throw(_("The payment for this membership is not paid. To generate invoice fill the payment details"))

		if self.invoice:
			vmraid.throw(_("An invoice is already linked to this document"))

		member = vmraid.get_doc("Member", self.member)
		if not member.customer:
			vmraid.throw(_("No customer linked to member {0}").format(vmraid.bold(self.member)))

		plan = vmraid.get_doc("Membership Type", self.membership_type)
		settings = vmraid.get_doc("Non Profit Settings")
		self.validate_membership_type_and_settings(plan, settings)

		invoice = make_invoice(self, member, plan, settings)
		self.reload()
		self.invoice = invoice.name

		if with_payment_entry:
			self.make_payment_entry(settings, invoice)

		if save:
			self.save()

		return invoice

	def validate_membership_type_and_settings(self, plan, settings):
		settings_link = get_link_to_form("Membership Type", self.membership_type)

		if not settings.membership_debit_account:
			vmraid.throw(_("You need to set <b>Debit Account</b> in {0}").format(settings_link))

		if not settings.company:
			vmraid.throw(_("You need to set <b>Default Company</b> for invoicing in {0}").format(settings_link))

		if not plan.linked_item:
			vmraid.throw(_("Please set a Linked Item for the Membership Type {0}").format(
				get_link_to_form("Membership Type", self.membership_type)))

	def make_payment_entry(self, settings, invoice):
		if not settings.membership_payment_account:
			vmraid.throw(_("You need to set <b>Payment Account</b> for Membership in {0}").format(
				get_link_to_form("Non Profit Settings", "Non Profit Settings")))

		from erpadda.accounts.doctype.payment_entry.payment_entry import get_payment_entry
		vmraid.flags.ignore_account_permission = True
		pe = get_payment_entry(dt="Sales Invoice", dn=invoice.name, bank_amount=invoice.grand_total)
		vmraid.flags.ignore_account_permission=False
		pe.paid_to = settings.membership_payment_account
		pe.reference_no = self.name
		pe.reference_date = getdate()
		pe.flags.ignore_mandatory = True
		pe.save()
		pe.submit()

	@vmraid.whitelist()
	def send_acknowlement(self):
		settings = vmraid.get_doc("Non Profit Settings")
		if not settings.send_email:
			vmraid.throw(_("You need to enable <b>Send Acknowledge Email</b> in {0}").format(
				get_link_to_form("Non Profit Settings", "Non Profit Settings")))

		member = vmraid.get_doc("Member", self.member)
		if not member.email_id:
			vmraid.throw(_("Email address of member {0} is missing").format(vmraid.utils.get_link_to_form("Member", self.member)))

		plan = vmraid.get_doc("Membership Type", self.membership_type)
		email = member.email_id
		attachments = [vmraid.attach_print("Membership", self.name, print_format=settings.membership_print_format)]

		if self.invoice and settings.send_invoice:
			attachments.append(vmraid.attach_print("Sales Invoice", self.invoice, print_format=settings.inv_print_format))

		email_template = vmraid.get_doc("Email Template", settings.email_template)
		context = { "doc": self, "member": member}

		email_args = {
			"recipients": [email],
			"message": vmraid.render_template(email_template.get("response"), context),
			"subject": vmraid.render_template(email_template.get("subject"), context),
			"attachments": attachments,
			"reference_doctype": self.doctype,
			"reference_name": self.name
		}

		if not vmraid.flags.in_test:
			vmraid.enqueue(method=vmraid.sendmail, queue="short", timeout=300, is_async=True, **email_args)
		else:
			vmraid.sendmail(**email_args)

	def generate_and_send_invoice(self):
		self.generate_invoice(save=False)
		self.send_acknowlement()


def make_invoice(membership, member, plan, settings):
	invoice = vmraid.get_doc({
		"doctype": "Sales Invoice",
		"customer": member.customer,
		"debit_to": settings.membership_debit_account,
		"currency": membership.currency,
		"company": settings.company,
		"is_pos": 0,
		"items": [
			{
				"item_code": plan.linked_item,
				"rate": membership.amount,
				"qty": 1
			}
		]
	})
	invoice.set_missing_values()
	invoice.insert()
	invoice.submit()

	vmraid.msgprint(_("Sales Invoice created successfully"))

	return invoice


def get_member_based_on_subscription(subscription_id, email):
	members = vmraid.get_all("Member", filters={
					"subscription_id": subscription_id,
					"email_id": email
				}, order_by="creation desc")

	try:
		return vmraid.get_doc("Member", members[0]["name"])
	except:
		return None


def verify_signature(data, endpoint="Membership"):
	if vmraid.flags.in_test or os.environ.get("CI"):
		return True
	signature = vmraid.request.headers.get("X-Razorpay-Signature")

	settings = vmraid.get_doc("Non Profit Settings")
	key = settings.get_webhook_secret(endpoint)

	controller = vmraid.get_doc("Razorpay Settings")

	controller.verify_signature(data, signature, key)
	vmraid.set_user(settings.creation_user)


@vmraid.whitelist(allow_guest=True)
def trigger_razorpay_subscription(*args, **kwargs):
	data = vmraid.request.get_data(as_text=True)
	try:
		verify_signature(data)
	except Exception as e:
		log = vmraid.log_error(e, "Membership Webhook Verification Error")
		notify_failure(log)
		return { "status": "Failed", "reason": e}

	if isinstance(data, six.string_types):
		data = json.loads(data)
	data = vmraid._dict(data)

	subscription = data.payload.get("subscription", {}).get("entity", {})
	subscription = vmraid._dict(subscription)

	payment = data.payload.get("payment", {}).get("entity", {})
	payment = vmraid._dict(payment)

	try:
		if not data.event == "subscription.charged":
			return

		member = get_member_based_on_subscription(subscription.id, payment.email)
		if not member:
			member = create_member(vmraid._dict({
				"fullname": payment.email,
				"email": payment.email,
				"plan_id": get_plan_from_razorpay_id(subscription.plan_id)
			}))

			member.subscription_id = subscription.id
			member.customer_id = payment.customer_id

			if subscription.get("notes"):
				member = get_additional_notes(member, subscription)

		company = get_company_for_memberships()
		# Update Membership
		membership = vmraid.new_doc("Membership")
		membership.update({
			"company": company,
			"member": member.name,
			"membership_status": "Current",
			"membership_type": member.membership_type,
			"currency": "INR",
			"paid": 1,
			"payment_id": payment.id,
			"from_date": datetime.fromtimestamp(subscription.current_start),
			"to_date": datetime.fromtimestamp(subscription.current_end),
			"amount": payment.amount / 100 # Convert to rupees from paise
		})
		membership.flags.ignore_mandatory = True
		membership.insert()

		# Update membership values
		member.subscription_start = datetime.fromtimestamp(subscription.start_at)
		member.subscription_end = datetime.fromtimestamp(subscription.end_at)
		member.subscription_activated = 1
		member.flags.ignore_mandatory = True
		member.save()

		settings = vmraid.get_doc("Non Profit Settings")
		if settings.allow_invoicing and settings.automate_membership_invoicing:
			membership.reload()
			membership.generate_invoice(with_payment_entry=settings.automate_membership_payment_entries, save=True)

	except Exception as e:
		message = "{0}\n\n{1}\n\n{2}: {3}".format(e, vmraid.get_traceback(), _("Payment ID"), payment.id)
		log = vmraid.log_error(message, _("Error creating membership entry for {0}").format(member.name))
		notify_failure(log)
		return { "status": "Failed", "reason": e}

	return { "status": "Success" }


def get_company_for_memberships():
	company = vmraid.db.get_single_value("Non Profit Settings", "company")
	if not company:
		from erpadda.healthcare.setup import get_company
		company = get_company()
	return company


def get_additional_notes(member, subscription):
	if type(subscription.notes) == dict:
		for k, v in subscription.notes.items():
			notes = "\n".join("{}: {}".format(k, v))

			# extract member name from notes
			if "name" in k.lower():
				member.update({
					"member_name": subscription.notes.get(k)
				})

			# extract pan number from notes
			if "pan" in k.lower():
				member.update({
					"pan_number": subscription.notes.get(k)
				})

		member.add_comment("Comment", notes)

	elif type(subscription.notes) == str:
		member.add_comment("Comment", subscription.notes)

	return member


def notify_failure(log):
	try:
		content = """
			Dear System Manager,
			Razorpay webhook for creating renewing membership subscription failed due to some reason.
			Please check the following error log linked below
			Error Log: {0}
			Regards, Administrator
		""".format(get_link_to_form("Error Log", log.name))

		sendmail_to_system_managers("[Important] [ERPAdda] Razorpay membership webhook failed , please check.", content)
	except:
		pass


def get_plan_from_razorpay_id(plan_id):
	plan = vmraid.get_all("Membership Type", filters={"razorpay_plan_id": plan_id}, order_by="creation desc")

	try:
		return plan[0]["name"]
	except:
		return None


def set_expired_status():
	vmraid.db.sql("""
		UPDATE
			`tabMembership` SET `status` = 'Expired'
		WHERE
			`status` not in ('Cancelled') AND `to_date` < %s
		""", (nowdate()))