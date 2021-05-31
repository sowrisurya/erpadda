# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("Stock Entry")
	vmraid.db.sql("update `tabStock Entry` set from_bom = if(ifnull(bom_no, '')='', 0, 1)")
