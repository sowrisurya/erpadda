# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.db.sql("""update `tabStock Entry` set purpose='Manufacture' where purpose='Manufacture/Repack' and ifnull(work_order,"")!="" """)
	vmraid.db.sql("""update `tabStock Entry` set purpose='Repack' where purpose='Manufacture/Repack' and ifnull(work_order,"")="" """)