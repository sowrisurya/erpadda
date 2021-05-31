# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.model.document import Document

class HRSettings(Document):
	def validate(self):
		self.set_naming_series()

	def set_naming_series(self):
		from erpadda.setup.doctype.naming_series.naming_series import set_by_naming_series
		set_by_naming_series("Employee", "employee_number",
			self.get("emp_created_by")=="Naming Series", hide_name_field=True)

