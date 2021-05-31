# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.model.document import Document
from vmraid.utils import cstr
from vmraid import _

class VitalSigns(Document):
	def validate(self):
		self.set_title()

	def set_title(self):
		self.title = _('{0} on {1}').format(self.patient_name or self.patient,
			vmraid.utils.format_date(self.signs_date))[:100]

