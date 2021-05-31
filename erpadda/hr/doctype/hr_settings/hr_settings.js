// Copyright (c) 2016, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('HR Settings', {
	restrict_backdated_leave_application: function(frm) {
		frm.toggle_reqd("role_allowed_to_create_backdated_leave_application", frm.doc.restrict_backdated_leave_application);
	}
});