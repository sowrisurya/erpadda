# -*- coding: utf-8 -*-
# Copyright (c) 2018, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid import _
from vmraid.model.document import Document
from vmraid.utils import getdate
from erpadda.hr.utils import update_employee

class EmployeePromotion(Document):
	def validate(self):
		if vmraid.get_value("Employee", self.employee, "status") == "Left":
			vmraid.throw(_("Cannot promote Employee with status Left"))

	def before_submit(self):
		if getdate(self.promotion_date) > getdate():
			vmraid.throw(_("Employee Promotion cannot be submitted before Promotion Date "),
				vmraid.DocstatusTransitionError)

	def on_submit(self):
		employee = vmraid.get_doc("Employee", self.employee)
		employee = update_employee(employee, self.promotion_details, date=self.promotion_date)
		employee.save()

	def on_cancel(self):
		employee = vmraid.get_doc("Employee", self.employee)
		employee = update_employee(employee, self.promotion_details, cancel=True)
		employee.save()
