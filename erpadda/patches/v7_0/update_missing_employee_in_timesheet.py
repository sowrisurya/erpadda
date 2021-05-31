from __future__ import unicode_literals
import vmraid

def execute():
	if vmraid.db.table_exists("Time Log") and "employee" in vmraid.db.get_table_columns("Time Log"):
		timesheet = vmraid.db.sql("""select tl.employee as employee, ts.name as name,
				tl.modified as modified, tl.modified_by as modified_by, tl.creation as creation, tl.owner as owner
			from 
				`tabTimesheet` ts, `tabTimesheet Detail` tsd, `tabTime Log` tl
			where 
				tsd.parent = ts.name and tl.from_time = tsd.from_time and tl.to_time = tsd.to_time 
				and tl.hours = tsd.hours and tl.billing_rate = tsd.billing_rate and tsd.idx=1 
				and tl.docstatus < 2 and (ts.employee = '' or ts.employee is null)""", as_dict=1)
		
		for data in timesheet:
			ts_doc = vmraid.get_doc('Timesheet', data.name)
			if len(ts_doc.time_logs) == 1:
				vmraid.db.sql(""" update `tabTimesheet` set creation = %(creation)s,
					owner = %(owner)s, modified = %(modified)s, modified_by = %(modified_by)s,
					employee = %(employee)s where name = %(name)s""", data)
