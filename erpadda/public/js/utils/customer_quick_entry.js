vmraid.provide('vmraid.ui.form');

vmraid.ui.form.CustomerQuickEntryForm = class CustomerQuickEntryForm extends vmraid.ui.form.QuickEntryForm {
	constructor(doctype, after_insert) {
		super(doctype, after_insert);
		this.skip_redirect_on_error = true;
	}

	render_dialog() {
		this.mandatory = this.mandatory.concat(this.get_variant_fields());
		super.render_dialog();
	}

	get_variant_fields() {
		var variant_fields = [{
			fieldtype: "Section Break",
			label: __("Primary Contact Details"),
			collapsible: 1
		},
		{
			label: __("Email Id"),
			fieldname: "email_id",
			fieldtype: "Data"
		},
		{
			fieldtype: "Column Break"
		},
		{
			label: __("Mobile Number"),
			fieldname: "mobile_no",
			fieldtype: "Data"
		},
		{
			fieldtype: "Section Break",
			label: __("Primary Address Details"),
			collapsible: 1
		},
		{
			label: __("Address Line 1"),
			fieldname: "address_line1",
			fieldtype: "Data"
		},
		{
			label: __("Address Line 2"),
			fieldname: "address_line2",
			fieldtype: "Data"
		},
		{
			label: __("ZIP Code"),
			fieldname: "pincode",
			fieldtype: "Data"
		},
		{
			fieldtype: "Column Break"
		},
		{
			label: __("City"),
			fieldname: "city",
			fieldtype: "Data"
		},
		{
			label: __("State"),
			fieldname: "state",
			fieldtype: "Data"
		},
		{
			label: __("Country"),
			fieldname: "country",
			fieldtype: "Link",
			options: "Country"
		},
		{
			label: __("Customer POS Id"),
			fieldname: "customer_pos_id",
			fieldtype: "Data",
			hidden: 1
		}];

		return variant_fields;
	}
}
