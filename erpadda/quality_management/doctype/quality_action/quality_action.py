# -*- coding: utf-8 -*-
# Copyright (c) 2018, VMRaid and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.model.document import Document

class QualityAction(Document):
	def validate(self):
		self.status = 'Open' if any([d.status=='Open' for d in self.resolutions]) else 'Completed'