# -*- coding: utf-8 -*-
# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.model.document import Document
from vmraid import _

class TrainingFeedback(Document):
	def validate(self):
		training_event = vmraid.get_doc("Training Event", self.training_event)
		if training_event.docstatus != 1:
			vmraid.throw(_('{0} must be submitted').format(_('Training Event')))

	def on_submit(self):
		training_event = vmraid.get_doc("Training Event", self.training_event)
		event_status = None
		for e in training_event.employees:
			if e.employee == self.employee:
				event_status = 'Feedback Submitted'
				break

		if event_status:
			vmraid.db.set_value("Training Event", self.training_event, "event_status", event_status)
