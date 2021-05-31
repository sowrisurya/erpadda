# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	for doctype in ("Material Request", "Purchase Order"):
		vmraid.reload_doctype(doctype)
		vmraid.reload_doctype(doctype + " Item")

		if not vmraid.db.has_column(doctype, "schedule_date"):
			continue

		#Update only submitted MR
		for record in vmraid.get_all(doctype, filters= [["docstatus", "=", 1]], fields=["name"]):
			doc = vmraid.get_doc(doctype, record)
			if doc.items:
				if not doc.schedule_date:
					schedule_dates = [d.schedule_date for d in doc.items if d.schedule_date]
					if len(schedule_dates) > 0:
						min_schedule_date = min(schedule_dates)
						vmraid.db.set_value(doctype, record,
							"schedule_date", min_schedule_date, update_modified=False)