# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	if "master_name" in vmraid.db.get_table_columns("Account"):	
		vmraid.db.sql("""update tabAccount set warehouse=master_name
			where ifnull(account_type, '') = 'Warehouse' and ifnull(master_name, '') != ''""")