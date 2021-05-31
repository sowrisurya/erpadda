// Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.provide("erpadda.accounts.dimensions");

vmraid.ui.form.on("Fees", {
	setup: function(frm) {
		frm.add_fetch("fee_structure", "receivable_account", "receivable_account");
		frm.add_fetch("fee_structure", "income_account", "income_account");
		frm.add_fetch("fee_structure", "cost_center", "cost_center");
	},

	company: function(frm) {
		erpadda.accounts.dimensions.update_dimension(frm, frm.doctype);
	},

	onload: function(frm) {
		frm.set_query("academic_term", function() {
			return{
				"filters": {
					"academic_year": (frm.doc.academic_year)
				}
			};
		});
		frm.set_query("fee_structure", function() {
			return{
				"filters":{
					"academic_year": (frm.doc.academic_year)
				}
			};
		});
		frm.set_query("receivable_account", function(doc) {
			return {
				filters: {
					'account_type': 'Receivable',
					'is_group': 0,
					'company': doc.company
				}
			};
		});
		frm.set_query("income_account", function(doc) {
			return {
				filters: {
					'account_type': 'Income Account',
					'is_group': 0,
					'company': doc.company
				}
			};
		});
		if (!frm.doc.posting_date) {
			frm.doc.posting_date = vmraid.datetime.get_today();
		}

		erpadda.accounts.dimensions.setup_dimension_filters(frm, frm.doctype);
	},

	refresh: function(frm) {
		if(frm.doc.docstatus == 0 && frm.doc.set_posting_time) {
			frm.set_df_property('posting_date', 'read_only', 0);
			frm.set_df_property('posting_time', 'read_only', 0);
		} else {
			frm.set_df_property('posting_date', 'read_only', 1);
			frm.set_df_property('posting_time', 'read_only', 1);
		}
		if(frm.doc.docstatus > 0) {
			frm.add_custom_button(__('Accounting Ledger'), function() {
				vmraid.route_options = {
					voucher_no: frm.doc.name,
					from_date: frm.doc.posting_date,
					to_date: moment(frm.doc.modified).format('YYYY-MM-DD'),
					company: frm.doc.company,
					group_by: '',
					show_cancelled_entries: frm.doc.docstatus === 2
				};
				vmraid.set_route("query-report", "General Ledger");
			}, __("View"));
			frm.add_custom_button(__("Payments"), function() {
				vmraid.set_route("List", "Payment Entry", {"Payment Entry Reference.reference_name": frm.doc.name});
			}, __("View"));
		}
		if(frm.doc.docstatus===1 && frm.doc.outstanding_amount>0) {
			frm.add_custom_button(__("Payment Request"), function() {
				frm.events.make_payment_request(frm);
			}, __('Create'));
			frm.page.set_inner_btn_group_as_primary(__('Create'));
		}
		if(frm.doc.docstatus===1 && frm.doc.outstanding_amount!=0) {
			frm.add_custom_button(__("Payment"), function() {
				frm.events.make_payment_entry(frm);
			}, __('Create'));
			frm.page.set_inner_btn_group_as_primary(__('Create'));
		}
	},

	student: function(frm) {
		if (frm.doc.student) {
			vmraid.call({
				method:"erpadda.education.api.get_current_enrollment",
				args: {
					"student": frm.doc.student,
					"academic_year": frm.doc.academic_year
				},
				callback: function(r) {
					if(r){
						$.each(r.message, function(i, d) {
							frm.set_value(i,d);
						});
					}
				}
			});
		}
	},

	make_payment_request: function(frm) {
		if (!frm.doc.student_email) {
			vmraid.msgprint(__("Please set the Email ID for the Student to send the Payment Request"));
		} else {
			vmraid.call({
				method:"erpadda.accounts.doctype.payment_request.payment_request.make_payment_request",
				args: {
					"dt": frm.doc.doctype,
					"dn": frm.doc.name,
					"party_type": "Student",
					"party": frm.doc.student,
					"recipient_id": frm.doc.student_email
				},
				callback: function(r) {
					if(!r.exc){
						var doc = vmraid.model.sync(r.message);
						vmraid.set_route("Form", doc[0].doctype, doc[0].name);
					}
				}
			});
		}
	},

	make_payment_entry: function(frm) {
		return vmraid.call({
			method: "erpadda.accounts.doctype.payment_entry.payment_entry.get_payment_entry",
			args: {
				"dt": frm.doc.doctype,
				"dn": frm.doc.name
			},
			callback: function(r) {
				var doc = vmraid.model.sync(r.message);
				vmraid.set_route("Form", doc[0].doctype, doc[0].name);
			}
		});
	},

	set_posting_time: function(frm) {
		frm.refresh();
	},

	academic_term: function() {
		vmraid.ui.form.trigger("Fees", "program");
	},

	fee_structure: function(frm) {
		frm.set_value("components" ,"");
		if (frm.doc.fee_structure) {
			vmraid.call({
				method: "erpadda.education.api.get_fee_components",
				args: {
					"fee_structure": frm.doc.fee_structure
				},
				callback: function(r) {
					if (r.message) {
						$.each(r.message, function(i, d) {
							var row = vmraid.model.add_child(frm.doc, "Fee Component", "components");
							row.fees_category = d.fees_category;
							row.description = d.description;
							row.amount = d.amount;
						});
					}
					refresh_field("components");
					frm.trigger("calculate_total_amount");
				}
			});
		}
	},

	calculate_total_amount: function(frm) {
		var grand_total = 0;
		for(var i=0;i<frm.doc.components.length;i++) {
			grand_total += frm.doc.components[i].amount;
		}
		frm.set_value("grand_total", grand_total);
	}
});


vmraid.ui.form.on("Fee Component", {
	amount: function(frm) {
		frm.trigger("calculate_total_amount");
	}
});
