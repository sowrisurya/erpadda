# -*- coding: utf-8 -*-
# Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid import _
from vmraid.model.document import Document
from vmraid import _

class Disease(Document):
	def validate(self):
		max_period = 0
		for task in self.treatment_task:
			# validate start_day is not > end_day
			if task.start_day > task.end_day:
				vmraid.throw(_("Start day is greater than end day in task '{0}'").format(task.task_name))
			# to calculate the period of the Crop Cycle
			if task.end_day > max_period: max_period = task.end_day
		self.treatment_period = max_period