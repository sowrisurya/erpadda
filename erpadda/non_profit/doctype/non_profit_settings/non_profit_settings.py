# -*- coding: utf-8 -*-
# Copyright (c) 2020, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid import _
from vmraid.integrations.utils import get_payment_gateway_controller
from vmraid.model.document import Document

class NonProfitSettings(Document):
	@vmraid.whitelist()
	def generate_webhook_secret(self, field="membership_webhook_secret"):
		key = vmraid.generate_hash(length=20)
		self.set(field, key)
		self.save()

		secret_for = "Membership" if field == "membership_webhook_secret" else "Donation"

		vmraid.msgprint(
			_("Here is your webhook secret for {0} API, this will be shown to you only once.").format(secret_for) + "<br><br>" + key,
			_("Webhook Secret")
		)

	@vmraid.whitelist()
	def revoke_key(self, key):
		self.set(key, None)
		self.save()

	def get_webhook_secret(self, endpoint="Membership"):
		fieldname = "membership_webhook_secret" if endpoint == "Membership" else "donation_webhook_secret"
		return self.get_password(fieldname=fieldname, raise_exception=False)

@vmraid.whitelist()
def get_plans_for_membership(*args, **kwargs):
	controller = get_payment_gateway_controller("Razorpay")
	plans = controller.get_plans()
	return [plan.get("item") for plan in plans.get("items")]