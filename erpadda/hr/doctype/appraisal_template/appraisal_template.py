# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.utils import cint, flt
from vmraid import _

from vmraid.model.document import Document

class AppraisalTemplate(Document):
	def validate(self):
		self.check_total_points()

	def check_total_points(self):
		total_points = 0
		for d in self.get("goals"):
			total_points += flt(d.per_weightage)

		if cint(total_points) != 100:
			vmraid.throw(_("Sum of points for all goals should be 100. It is {0}").format(total_points))
