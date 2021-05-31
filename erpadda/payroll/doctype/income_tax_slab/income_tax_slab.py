# -*- coding: utf-8 -*-
# Copyright (c) 2020, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
#import vmraid
import erpadda
from vmraid.model.document import Document

class IncomeTaxSlab(Document):
	def validate(self):
		if self.company:
			self.currency = erpadda.get_company_currency(self.company)
