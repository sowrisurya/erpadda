// Copyright (c) 2016, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('Training Event', {
	onload_post_render: function(frm) {
		frm.get_field("employees").grid.set_multiple_add("employee");
	},
	refresh: function(frm) {
		if(!frm.doc.__islocal) {
			frm.add_custom_button(__("Training Result"), function() {
				vmraid.route_options = {
					training_event: frm.doc.name
				}
				vmraid.set_route("List", "Training Result");
			});
			frm.add_custom_button(__("Training Feedback"), function() {
				vmraid.route_options = {
					training_event: frm.doc.name
				}
				vmraid.set_route("List", "Training Feedback");
			});
		}
	}
});
