# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.db.sql('''UPDATE `tabDocType` SET module="Core" 
				WHERE name IN ("SMS Parameter", "SMS Settings");''')