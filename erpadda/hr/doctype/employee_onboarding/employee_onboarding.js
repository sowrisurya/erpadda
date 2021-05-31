// Copyright (c) 2018, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('Employee Onboarding', {
	setup: function(frm) {
		frm.add_fetch("employee_onboarding_template", "company", "company");
		frm.add_fetch("employee_onboarding_template", "department", "department");
		frm.add_fetch("employee_onboarding_template", "designation", "designation");
		frm.add_fetch("employee_onboarding_template", "employee_grade", "employee_grade");


		frm.set_query("job_applicant", function () {
			return {
				filters:{
					"status": "Accepted",
				}
			};
		});

		frm.set_query('job_offer', function () {
			return {
				filters: {
					'job_applicant': frm.doc.job_applicant,
					'docstatus': 1
				}
			};
		});
	},

	refresh: function(frm) {
		if (frm.doc.employee) {
			frm.add_custom_button(__('Employee'), function() {
				vmraid.set_route("Form", "Employee", frm.doc.employee);
			},__("View"));
		}
		if (frm.doc.project) {
			frm.add_custom_button(__('Project'), function() {
				vmraid.set_route("Form", "Project", frm.doc.project);
			},__("View"));
			frm.add_custom_button(__('Task'), function() {
				vmraid.set_route('List', 'Task', {project: frm.doc.project});
			},__("View"));
		}
		if ((!frm.doc.employee) && (frm.doc.docstatus === 1)) {
			frm.add_custom_button(__('Employee'), function () {
				vmraid.model.open_mapped_doc({
					method: "erpadda.hr.doctype.employee_onboarding.employee_onboarding.make_employee",
					frm: frm
				});
			}, __('Create'));
			frm.page.set_inner_btn_group_as_primary(__('Create'));
		}
		if (frm.doc.docstatus === 1 && frm.doc.project) {
			vmraid.call({
				method: "erpadda.hr.utils.get_boarding_status",
				args: {
					"project": frm.doc.project
				},
				callback: function(r) {
					if (r.message) {
						frm.set_value('boarding_status', r.message);
					}
					refresh_field("boarding_status");
				}
			});
		}

	},

	employee_onboarding_template: function(frm) {
		frm.set_value("activities" ,"");
		if (frm.doc.employee_onboarding_template) {
			vmraid.call({
				method: "erpadda.hr.utils.get_onboarding_details",
				args: {
					"parent": frm.doc.employee_onboarding_template,
					"parenttype": "Employee Onboarding Template"
				},
				callback: function(r) {
					if (r.message) {
						r.message.forEach((d) => {
							frm.add_child("activities", d);
						});
						refresh_field("activities");
					}
				}
			});
		}
	}
});
