// Copyright (c) 2019, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('DATEV Settings', {
	refresh: function(frm) {
		frm.add_custom_button('Show Report', () => vmraid.set_route('query-report', 'DATEV'), "fa fa-table");
	}
});
