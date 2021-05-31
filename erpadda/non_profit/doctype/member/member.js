// Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('Member', {
	setup: function(frm) {
		vmraid.db.get_single_value('Non Profit Settings', 'enable_razorpay_for_memberships').then(val => {
			if (val && (frm.doc.subscription_id || frm.doc.customer_id)) {
				frm.set_df_property('razorpay_details_section', 'hidden', false);
			}
		})
	},

	refresh: function(frm) {

		vmraid.dynamic_link = {doc: frm.doc, fieldname: 'name', doctype: 'Member'};

		frm.toggle_display(['address_html','contact_html'], !frm.doc.__islocal);

		if(!frm.doc.__islocal) {
			vmraid.contacts.render_address_and_contact(frm);

			// custom buttons
			frm.add_custom_button(__('Accounting Ledger'), function() {
				vmraid.set_route('query-report', 'General Ledger',
					{party_type:'Member', party:frm.doc.name});
			});

			frm.add_custom_button(__('Accounts Receivable'), function() {
				vmraid.set_route('query-report', 'Accounts Receivable', {member:frm.doc.name});
			});

			if (!frm.doc.customer) {
				frm.add_custom_button(__('Create Customer'), () => {
					frm.call('make_customer_and_link').then(() => {
						frm.reload_doc();
					});
				});
			}

			// indicator
			erpadda.utils.set_party_dashboard_indicators(frm);

		} else {
			vmraid.contacts.clear_address_and_contact(frm);
		}

		vmraid.call({
			method:"vmraid.client.get_value",
			args:{
				'doctype':"Membership",
				'filters':{'member': frm.doc.name},
				'fieldname':[
					'to_date'
				]
			},
			callback: function (data) {
				if(data.message) {
					vmraid.model.set_value(frm.doctype,frm.docname,
						"membership_expiry_date", data.message.to_date);
				}
			}
		});
	}
});