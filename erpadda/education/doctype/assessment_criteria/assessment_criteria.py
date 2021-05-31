# -*- coding: utf-8 -*-
# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid import _
from vmraid.model.document import Document

STD_CRITERIA = ["total", "total score", "total grade", "maximum score", "score", "grade"]

class AssessmentCriteria(Document):
	def validate(self):
		if self.assessment_criteria.lower() in STD_CRITERIA:
			vmraid.throw(_("Can't create standard criteria. Please rename the criteria"))