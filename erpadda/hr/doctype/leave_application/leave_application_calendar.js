// Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

vmraid.views.calendar["Leave Application"] = {
	field_map: {
		"start": "from_date",
		"end": "to_date",
		"id": "name",
		"title": "title",
		"docstatus": 1
	},
	options: {
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month'
		}
	},
	get_events_method: "erpadda.hr.doctype.leave_application.leave_application.get_events"
}