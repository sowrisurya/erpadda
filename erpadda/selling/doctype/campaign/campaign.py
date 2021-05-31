# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

from vmraid.model.document import Document
from vmraid.model.naming import set_name_by_naming_series

class Campaign(Document):
	def autoname(self):
		if vmraid.defaults.get_global_default('campaign_naming_by') != 'Naming Series':
			self.name = self.campaign_name
		else:
			set_name_by_naming_series(self)
