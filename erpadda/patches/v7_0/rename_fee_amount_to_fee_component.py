# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

from vmraid.model.utils.rename_field import rename_field

def execute():
	if vmraid.db.exists("DocType", "Fee Amount"):
		vmraid.rename_doc("DocType", "Fee Amount", "Fee Component")
		for dt in ("Fees", "Fee Structure"):
			vmraid.reload_doctype(dt)
			rename_field(dt, "amount", "components")
		
	