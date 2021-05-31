# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	for si in vmraid.db.sql_list("""select name
		from `tabSales Invoice`
		where ifnull(update_stock,0) = 1 and docstatus = 1 and exists(
			select name from `tabSales Invoice Item` where parent=`tabSales Invoice`.name and
				ifnull(so_detail, "") != "")"""):

		invoice = vmraid.get_doc("Sales Invoice", si)
		invoice.update_qty()
