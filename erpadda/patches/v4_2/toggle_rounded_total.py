# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	global_defaults = vmraid.get_doc("Global Defaults", "Global Defaults")
	global_defaults.toggle_rounded_total()
