# -*- coding: utf-8 -*-
# Copyright (c) 2019, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from vmraid.model.document import Document
import requests
import vmraid
from vmraid import _

class ExotelSettings(Document):
	def validate(self):
		self.verify_credentials()

	def verify_credentials(self):
		if self.enabled:
			response = requests.get('https://api.exotel.com/v1/Accounts/{sid}'
				.format(sid = self.account_sid), auth=(self.api_key, self.api_token))
			if response.status_code != 200:
				vmraid.throw(_("Invalid credentials"))