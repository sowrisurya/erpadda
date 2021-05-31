from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('projects', 'doctype', 'timesheet_detail')
	vmraid.reload_doc('accounts', 'doctype', 'sales_invoice_timesheet')

	vmraid.db.sql(""" update 
			`tabTimesheet` as ts, 
		(select 
			sum(billing_amount) as billing_amount, sum(billing_hours) as billing_hours, time_sheet 
			from `tabSales Invoice Timesheet` where docstatus = 1 group by time_sheet
		) as sit
		set 
			ts.total_billed_amount = sit.billing_amount, ts.total_billed_hours = sit.billing_hours, 
			ts.per_billed = ((sit.billing_amount * 100)/ts.total_billable_amount)
		where ts.name = sit.time_sheet and ts.docstatus = 1""")

	vmraid.db.sql(""" update `tabTimesheet Detail` tsd, `tabTimesheet` ts set tsd.sales_invoice = ts.sales_invoice
		where tsd.parent = ts.name and ts.sales_invoice is not null""")