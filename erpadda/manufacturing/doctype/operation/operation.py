# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from vmraid.model.document import Document

class Operation(Document):
	def validate(self):
		if not self.description:
			self.description = self.name
