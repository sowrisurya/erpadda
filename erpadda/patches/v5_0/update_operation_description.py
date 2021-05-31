# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
import vmraid.permissions

def execute():
	if "opn_description" in vmraid.db.get_table_columns("BOM Operation"):
		vmraid.db.sql("""update `tabBOM Operation` set description = opn_description
			where ifnull(description, '') = ''""")