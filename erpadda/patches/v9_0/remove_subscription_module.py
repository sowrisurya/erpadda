# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	if vmraid.db.exists('Module Def', 'Subscription'):
		vmraid.db.sql(""" delete from `tabModule Def` where name = 'Subscription'""")