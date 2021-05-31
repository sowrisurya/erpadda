# -*- coding: utf-8 -*-
# Copyright (c) 2019, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.model.document import Document

class QualityFeedback(Document):
	@vmraid.whitelist()
	def set_parameters(self):
		if self.template and not getattr(self, 'parameters', []):
			for d in vmraid.get_doc('Quality Feedback Template', self.template).parameters:
				self.append('parameters', dict(
					parameter = d.parameter,
					rating = 1
				))

	def validate(self):
		if not self.document_name:
			self.document_type ='User'
			self.document_name = vmraid.session.user
		self.set_parameters()

