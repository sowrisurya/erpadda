// Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

vmraid.provide("erpadda.maintenance");

vmraid.ui.form.on('Maintenance Schedule', {
	setup: function(frm) {
		frm.set_query('contact_person', erpadda.queries.contact_query);
		frm.set_query('customer_address', erpadda.queries.address_query);
		frm.set_query('customer', erpadda.queries.customer);

		frm.add_fetch('item_code', 'item_name', 'item_name');
		frm.add_fetch('item_code', 'description', 'description');
	},
	onload: function(frm) {
		if (!frm.doc.status) {
			frm.set_value({status:'Draft'});
		}
		if (frm.doc.__islocal) {
			frm.set_value({transaction_date: vmraid.datetime.get_today()});
		}
	},
	refresh: function(frm) {
		setTimeout(() => {
			frm.toggle_display('generate_schedule', !(frm.is_new()));
			frm.toggle_display('schedule', !(frm.is_new()));
		},10);
	},
	customer: function(frm) {
		erpadda.utils.get_party_details(frm)
	},
	customer_address: function(frm) {
		erpadda.utils.get_address_display(frm, 'customer_address', 'address_display');
	},
	contact_person: function(frm) {
		erpadda.utils.get_contact_details(frm);
	},
	generate_schedule: function(frm) {
		if (frm.is_new()) {
			vmraid.msgprint(__('Please save first'));
		} else {
			frm.call('generate_schedule');
		}
	}
})

// TODO commonify this code
erpadda.maintenance.MaintenanceSchedule = class MaintenanceSchedule extends vmraid.ui.form.Controller {
	refresh() {
		vmraid.dynamic_link = {doc: this.frm.doc, fieldname: 'customer', doctype: 'Customer'}

		var me = this;

		if (this.frm.doc.docstatus === 0) {
			this.frm.add_custom_button(__('Sales Order'),
				function() {
					erpadda.utils.map_current_doc({
						method: "erpadda.selling.doctype.sales_order.sales_order.make_maintenance_schedule",
						source_doctype: "Sales Order",
						target: me.frm,
						setters: {
							customer: me.frm.doc.customer || undefined
						},
						get_query_filters: {
							docstatus: 1,
							company: me.frm.doc.company
						}
					});
				}, __("Get Items From"));
		} else if (this.frm.doc.docstatus === 1) {
			this.frm.add_custom_button(__('Create Maintenance Visit'), function() {
				vmraid.model.open_mapped_doc({
					method: "erpadda.maintenance.doctype.maintenance_schedule.maintenance_schedule.make_maintenance_visit",
					source_name: me.frm.doc.name,
					frm: me.frm
				});
			}, __('Create'));
		}
	}

	start_date(doc, cdt, cdn) {
		this.set_no_of_visits(doc, cdt, cdn);
	}

	end_date(doc, cdt, cdn) {
		this.set_no_of_visits(doc, cdt, cdn);
	}

	periodicity(doc, cdt, cdn) {
		this.set_no_of_visits(doc, cdt, cdn);
	}

	set_no_of_visits(doc, cdt, cdn) {
		var item = vmraid.get_doc(cdt, cdn);

		if (item.start_date && item.end_date && item.periodicity) {
			if(item.start_date > item.end_date) {
				vmraid.msgprint(__("Row {0}:Start Date must be before End Date", [item.idx]));
				return;
			}

			var date_diff = vmraid.datetime.get_diff(item.end_date, item.start_date) + 1;

			var days_in_period = {
				"Weekly": 7,
				"Monthly": 30,
				"Quarterly": 91,
				"Half Yearly": 182,
				"Yearly": 365
			}

			var no_of_visits = cint(date_diff / days_in_period[item.periodicity]);
			vmraid.model.set_value(item.doctype, item.name, "no_of_visits", no_of_visits);
		}
	}
};

extend_cscript(cur_frm.cscript, new erpadda.maintenance.MaintenanceSchedule({frm: cur_frm}));

