# -*- coding: utf-8 -*-
# Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from vmraid.model.document import Document
from vmraid.contacts.address_and_contact import load_address_and_contact

class Donor(Document):
	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)

	def validate(self):
		from vmraid.utils import validate_email_address
		if self.email:
			validate_email_address(self.email.strip(), True)

