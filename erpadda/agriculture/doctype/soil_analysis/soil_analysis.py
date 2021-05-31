# -*- coding: utf-8 -*-
# Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.model.document import Document

class SoilAnalysis(Document):
	@vmraid.whitelist()
	def load_contents(self):
		docs = vmraid.get_all("Agriculture Analysis Criteria", filters={'linked_doctype':'Soil Analysis'})
		for doc in docs:
			self.append('soil_analysis_criteria', {'title': str(doc.name)})