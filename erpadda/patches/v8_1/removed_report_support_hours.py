# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.db.sql(""" update `tabAuto Email Report` set report = %s
		where name = %s""", ('Support Hour Distribution', 'Support Hours'))

	vmraid.db.sql(""" update `tabCustom Role` set report = %s
		where report = %s""", ('Support Hour Distribution', 'Support Hours'))

	vmraid.delete_doc('Report', 'Support Hours')