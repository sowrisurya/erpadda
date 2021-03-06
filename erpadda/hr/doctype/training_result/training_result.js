// Copyright (c) 2016, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('Training Result', {
	onload: function(frm) {
		frm.trigger("training_event");
	},

	training_event: function(frm) {
		frm.trigger("training_event");
	},

	training_event: function(frm) {
		if (frm.doc.training_event && !frm.doc.docstatus && !frm.doc.employees) { 
			vmraid.call({
				method: "erpadda.hr.doctype.training_result.training_result.get_employees",
				args: {
					"training_event": frm.doc.training_event
				},
				callback: function(r) {
					frm.set_value("employees" ,"");
					if (r.message) {
						$.each(r.message, function(i, d) {
							var row = vmraid.model.add_child(cur_frm.doc, "Training Result Employee", "employees");
							row.employee = d.employee;
							row.employee_name = d.employee_name;
						});
					}
					refresh_field("employees");
				}
			});
		}
	}
});
