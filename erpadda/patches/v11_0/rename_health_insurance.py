# Copyright (c) 2018, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.rename_doc('DocType', 'Health Insurance', 'Employee Health Insurance', force=True)
	vmraid.reload_doc('hr', 'doctype', 'employee_health_insurance')