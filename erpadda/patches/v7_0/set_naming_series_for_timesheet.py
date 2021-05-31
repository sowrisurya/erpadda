# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import vmraid
from vmraid.custom.doctype.property_setter.property_setter import make_property_setter

def execute():
	vmraid.reload_doc('projects', 'doctype', 'timesheet')
	vmraid.reload_doc('projects', 'doctype', 'timesheet_detail')
	vmraid.reload_doc('accounts', 'doctype', 'sales_invoice_timesheet')
	
	make_property_setter('Timesheet', "naming_series", "options", 'TS-', "Text")
	make_property_setter('Timesheet', "naming_series", "default", 'TS-', "Text")