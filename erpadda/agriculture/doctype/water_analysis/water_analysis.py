# -*- coding: utf-8 -*-
# Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid import _
from vmraid.model.document import Document
from vmraid import _

class WaterAnalysis(Document):
	@vmraid.whitelist()
	def load_contents(self):
		docs = vmraid.get_all("Agriculture Analysis Criteria", filters={'linked_doctype':'Water Analysis'})
		for doc in docs:
			self.append('water_analysis_criteria', {'title': str(doc.name)})

	@vmraid.whitelist()
	def update_lab_result_date(self):
		if not self.result_datetime:
			self.result_datetime = self.laboratory_testing_datetime

	def validate(self):
		if self.collection_datetime > self.laboratory_testing_datetime:
			vmraid.throw(_('Lab testing datetime cannot be before collection datetime'))
		if self.laboratory_testing_datetime > self.result_datetime:
			vmraid.throw(_('Lab result datetime cannot be before testing datetime'))