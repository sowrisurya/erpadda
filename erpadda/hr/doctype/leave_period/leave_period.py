# -*- coding: utf-8 -*-
# Copyright (c) 2018, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid import _
from vmraid.utils import getdate, cstr, add_days, date_diff, getdate, ceil
from vmraid.model.document import Document
from erpadda.hr.utils import validate_overlap
from vmraid.utils.background_jobs import enqueue

class LeavePeriod(Document):

	def validate(self):
		self.validate_dates()
		validate_overlap(self, self.from_date, self.to_date, self.company)

	def validate_dates(self):
		if getdate(self.from_date) >= getdate(self.to_date):
			vmraid.throw(_("To date can not be equal or less than from date"))
