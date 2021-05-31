# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.utils.dashboard import cache_source

@vmraid.whitelist()
@cache_source
def get(chart_name = None, chart = None, no_cache = None, filters = None, from_date = None,
	to_date = None, timespan = None, time_interval = None, heatmap_year = None):
	if chart_name:
		chart = vmraid.get_doc('Dashboard Chart', chart_name)
	else:
		chart = vmraid._dict(vmraid.parse_json(chart))

	filters = vmraid.parse_json(filters)

	data = vmraid.db.get_list('Medical Department', fields=['name'])
	if not filters:
		filters = {}

	status = ['Open', 'Scheduled', 'Closed', 'Cancelled']
	for department in data:
		filters['department'] = department.name
		department['total_appointments'] = vmraid.db.count('Patient Appointment', filters=filters)

		for entry in status:
			filters['status'] = entry
			department[vmraid.scrub(entry)] = vmraid.db.count('Patient Appointment', filters=filters)
		filters.pop('status')

	sorted_department_map = sorted(data, key = lambda i: i['total_appointments'], reverse=True)

	if len(sorted_department_map) > 10:
		sorted_department_map = sorted_department_map[:10]

	labels = []
	open_appointments = []
	scheduled = []
	closed = []
	cancelled = []

	for department in sorted_department_map:
		labels.append(department.name)
		open_appointments.append(department.open)
		scheduled.append(department.scheduled)
		closed.append(department.closed)
		cancelled.append(department.cancelled)

	return {
		'labels': labels,
		'datasets': [
			{
				'name': 'Open',
				'values': open_appointments
			},
			{
				'name': 'Scheduled',
				'values': scheduled
			},
			{
				'name': 'Closed',
				'values': closed
			},
			{
				'name': 'Cancelled',
				'values': cancelled
			}
		],
		'type': 'bar'
	}