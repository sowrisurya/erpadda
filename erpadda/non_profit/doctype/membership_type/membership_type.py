# -*- coding: utf-8 -*-
# Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from vmraid.model.document import Document
import vmraid
from vmraid import _

class MembershipType(Document):
	def validate(self):
		if self.linked_item:
			is_stock_item = vmraid.db.get_value("Item", self.linked_item, "is_stock_item")
			if is_stock_item:
				vmraid.throw(_("The Linked Item should be a service item"))

def get_membership_type(razorpay_id):
	return vmraid.db.exists("Membership Type", {"razorpay_plan_id": razorpay_id})