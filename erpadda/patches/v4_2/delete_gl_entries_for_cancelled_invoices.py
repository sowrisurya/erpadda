# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	cancelled_invoices = vmraid.db.sql_list("""select name from `tabSales Invoice` 
		where docstatus = 2 and ifnull(update_stock, 0) = 1""")

	if cancelled_invoices:
		vmraid.db.sql("""delete from `tabGL Entry` 
			where voucher_type = 'Sales Invoice' and voucher_no in (%s)""" 
			% (', '.join(['%s']*len(cancelled_invoices))), tuple(cancelled_invoices))