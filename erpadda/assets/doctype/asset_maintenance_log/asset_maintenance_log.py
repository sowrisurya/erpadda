# -*- coding: utf-8 -*-
# Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.model.document import Document
from vmraid import _
from vmraid.utils import nowdate, getdate
from erpadda.assets.doctype.asset_maintenance.asset_maintenance import calculate_next_due_date

class AssetMaintenanceLog(Document):
	def validate(self):
		if getdate(self.due_date) < getdate(nowdate()) and self.maintenance_status not in ["Completed", "Cancelled"]:
			self.maintenance_status = "Overdue"

		if self.maintenance_status == "Completed" and not self.completion_date:
			vmraid.throw(_("Please select Completion Date for Completed Asset Maintenance Log"))

		if self.maintenance_status != "Completed" and self.completion_date:
			vmraid.throw(_("Please select Maintenance Status as Completed or remove Completion Date"))

	def on_submit(self):
		if self.maintenance_status not in ['Completed', 'Cancelled']:
			vmraid.throw(_("Maintenance Status has to be Cancelled or Completed to Submit"))
		self.update_maintenance_task()

	def update_maintenance_task(self):
		asset_maintenance_doc = vmraid.get_doc('Asset Maintenance Task', self.task)
		if self.maintenance_status == "Completed":
			if asset_maintenance_doc.last_completion_date != self.completion_date:
				next_due_date = calculate_next_due_date(periodicity = self.periodicity, last_completion_date = self.completion_date)
				asset_maintenance_doc.last_completion_date = self.completion_date
				asset_maintenance_doc.next_due_date = next_due_date
				asset_maintenance_doc.maintenance_status = "Planned"
				asset_maintenance_doc.save()
		if self.maintenance_status == "Cancelled":
			asset_maintenance_doc.maintenance_status = "Cancelled"
			asset_maintenance_doc.save()
		asset_maintenance_doc = vmraid.get_doc('Asset Maintenance', self.asset_maintenance)
		asset_maintenance_doc.save()

@vmraid.whitelist()
@vmraid.validate_and_sanitize_search_inputs
def get_maintenance_tasks(doctype, txt, searchfield, start, page_len, filters):
	asset_maintenance_tasks = vmraid.db.get_values('Asset Maintenance Task', {'parent':filters.get("asset_maintenance")}, 'maintenance_task')
	return asset_maintenance_tasks
