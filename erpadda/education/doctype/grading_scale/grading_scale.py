# -*- coding: utf-8 -*-
# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid import _
from vmraid.utils import cint
from vmraid.model.document import Document

class GradingScale(Document):
	def validate(self):
		thresholds = []
		for d in self.intervals:
			if d.threshold in thresholds:
				vmraid.throw(_("Treshold {0}% appears more than once").format(d.threshold))
			else:
				thresholds.append(cint(d.threshold))
		if 0 not in thresholds:
			vmraid.throw(_("Please define grade for Threshold 0%"))