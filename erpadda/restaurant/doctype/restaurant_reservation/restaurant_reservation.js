// Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('Restaurant Reservation', {
	setup: function(frm) {
		frm.add_fetch('customer', 'customer_name', 'customer_name');
	},
	refresh: function(frm) {

	}
});
