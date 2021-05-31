// Copyright (c) 2018, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('Shift Type', {
	refresh: function(frm) {
		frm.add_custom_button(
			'Mark Attendance',
			() => frm.call({
				doc: frm.doc,
				method: 'process_auto_attendance',
				freeze: true,
				callback: () => {
					vmraid.msgprint(__("Attendance has been marked as per employee check-ins"));
				}
			})
		);
	}
});
