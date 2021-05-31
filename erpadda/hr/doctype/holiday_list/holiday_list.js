// Copyright (c) 2016, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('Holiday List', {
	refresh: function(frm) {
		if (frm.doc.holidays) {
			frm.set_value('total_holidays', frm.doc.holidays.length);
		}
	},
	from_date: function(frm) {
		if (frm.doc.from_date && !frm.doc.to_date) {
			var a_year_from_start = vmraid.datetime.add_months(frm.doc.from_date, 12);
			frm.set_value("to_date", vmraid.datetime.add_days(a_year_from_start, -1));
		}
	}
});
