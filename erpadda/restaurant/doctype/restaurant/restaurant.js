// Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('Restaurant', {
	refresh: function(frm) {
		frm.add_custom_button(__('Order Entry'), () => {
			vmraid.set_route('Form', 'Restaurant Order Entry');
		});
	}
});
