# -*- coding: utf-8 -*-
# Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid import _
from vmraid.utils import time_diff_in_hours
from vmraid.model.document import Document

class AssetRepair(Document):
	def validate(self):
		if self.repair_status == "Completed" and not self.completion_date:
			vmraid.throw(_("Please select Completion Date for Completed Repair"))


@vmraid.whitelist()
def get_downtime(failure_date, completion_date):
	downtime = time_diff_in_hours(completion_date, failure_date)
	return round(downtime, 2)