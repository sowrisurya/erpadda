// Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('Volunteer', {
	refresh: function(frm) {

		vmraid.dynamic_link = {doc: frm.doc, fieldname: 'name', doctype: 'Volunteer'};

		frm.toggle_display(['address_html','contact_html'], !frm.doc.__islocal);

		if(!frm.doc.__islocal) {
			vmraid.contacts.render_address_and_contact(frm);
		} else {
			vmraid.contacts.clear_address_and_contact(frm);
		}
	}
});
