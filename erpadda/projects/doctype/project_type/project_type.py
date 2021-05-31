# -*- coding: utf-8 -*-
# Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from vmraid.model.document import Document
import vmraid
from vmraid import _

class ProjectType(Document):
	def on_trash(self):
		if self.name == "External":
			vmraid.throw(_("You cannot delete Project Type 'External'"))