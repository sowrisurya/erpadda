// Copyright (c) 2016, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('Products Settings', {
	refresh: function(frm) {
		vmraid.model.with_doctype('Item', () => {
			const item_meta = vmraid.get_meta('Item');

			const valid_fields = item_meta.fields.filter(
				df => ['Link', 'Table MultiSelect'].includes(df.fieldtype) && !df.hidden
			).map(df => ({ label: df.label, value: df.fieldname }));

			frm.fields_dict.filter_fields.grid.update_docfield_property(
				'fieldname', 'fieldtype', 'Select'
			);
			frm.fields_dict.filter_fields.grid.update_docfield_property(
				'fieldname', 'options', valid_fields
			);
		});
	}
});
