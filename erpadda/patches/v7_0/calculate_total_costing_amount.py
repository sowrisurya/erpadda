from __future__ import unicode_literals
import vmraid
from vmraid.utils import flt

def execute():
	vmraid.reload_doc('projects', 'doctype', 'timesheet')

	for data in vmraid.get_all('Timesheet', fields=["name, total_costing_amount"],
		filters = [["docstatus", "<", "2"]]):
		if flt(data.total_costing_amount) == 0.0:
			ts = vmraid.get_doc('Timesheet', data.name)
			ts.update_cost()
			ts.calculate_total_amounts()
			ts.flags.ignore_validate = True
			ts.flags.ignore_mandatory = True
			ts.flags.ignore_validate_update_after_submit = True
			ts.flags.ignore_links = True
			ts.save()
