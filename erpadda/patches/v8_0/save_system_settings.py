# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.utils import cint

def execute():
	"""
		save system settings document
	"""

	vmraid.reload_doc("core", "doctype", "system_settings")
	doc = vmraid.get_doc("System Settings")
	doc.flags.ignore_mandatory = True

	if cint(doc.currency_precision) == 0:
		doc.currency_precision = ''

	doc.save(ignore_permissions=True)
