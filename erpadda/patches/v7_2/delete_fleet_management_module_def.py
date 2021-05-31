# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	if vmraid.db.exists('Module Def', 'Fleet Management'):
		vmraid.db.sql("""delete from `tabModule Def`
			where module_name = 'Fleet Management'""")