// Copyright (c) 2019, VMRaid Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

vmraid.provide("erpadda");
cur_frm.email_field = "email_id";

erpadda.LeadController = class LeadController extends vmraid.ui.form.Controller {
	setup () {
		this.frm.make_methods = {
			'Customer': this.make_customer,
			'Quotation': this.make_quotation,
			'Opportunity': this.make_opportunity
		};

		this.frm.toggle_reqd("lead_name", !this.frm.doc.organization_lead);
	}

	onload () {
		this.frm.set_query("customer", function (doc, cdt, cdn) {
			return { query: "erpadda.controllers.queries.customer_query" }
		});

		this.frm.set_query("lead_owner", function (doc, cdt, cdn) {
			return { query: "vmraid.core.doctype.user.user.user_query" }
		});

		this.frm.set_query("contact_by", function (doc, cdt, cdn) {
			return { query: "vmraid.core.doctype.user.user.user_query" }
		});
	}

	refresh () {
		let doc = this.frm.doc;
		erpadda.toggle_naming_series();
		vmraid.dynamic_link = { doc: doc, fieldname: 'name', doctype: 'Lead' }

		if (!this.frm.is_new() && doc.__onload && !doc.__onload.is_customer) {
			this.frm.add_custom_button(__("Customer"), this.make_customer, __("Create"));
			this.frm.add_custom_button(__("Opportunity"), this.make_opportunity, __("Create"));
			this.frm.add_custom_button(__("Quotation"), this.make_quotation, __("Create"));
		}

		if (!this.frm.is_new()) {
			vmraid.contacts.render_address_and_contact(this.frm);
		} else {
			vmraid.contacts.clear_address_and_contact(this.frm);
		}
	}

	make_customer () {
		vmraid.model.open_mapped_doc({
			method: "erpadda.crm.doctype.lead.lead.make_customer",
			frm: cur_frm
		})
	}

	make_opportunity () {
		vmraid.model.open_mapped_doc({
			method: "erpadda.crm.doctype.lead.lead.make_opportunity",
			frm: cur_frm
		})
	}

	make_quotation () {
		vmraid.model.open_mapped_doc({
			method: "erpadda.crm.doctype.lead.lead.make_quotation",
			frm: cur_frm
		})
	}

	organization_lead () {
		this.frm.toggle_reqd("lead_name", !this.frm.doc.organization_lead);
		this.frm.toggle_reqd("company_name", this.frm.doc.organization_lead);
	}

	company_name () {
		if (this.frm.doc.organization_lead && !this.frm.doc.lead_name) {
			this.frm.set_value("lead_name", this.frm.doc.company_name);
		}
	}

	contact_date () {
		if (this.frm.doc.contact_date) {
			let d = moment(this.frm.doc.contact_date);
			d.add(1, "day");
			this.frm.set_value("ends_on", d.format(vmraid.defaultDatetimeFormat));
		}
	}
};

extend_cscript(cur_frm.cscript, new erpadda.LeadController({ frm: cur_frm }));
