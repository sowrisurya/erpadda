# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('stock', 'doctype', 'delivery_note_item')

	vmraid.db.sql("""update `tabDelivery Note Item` set so_detail = prevdoc_detail_docname
		where ifnull(against_sales_order, '') != ''""")

	vmraid.db.sql("""update `tabDelivery Note Item` set si_detail = prevdoc_detail_docname
		where ifnull(against_sales_invoice, '') != ''""")
