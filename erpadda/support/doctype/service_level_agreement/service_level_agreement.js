// Copyright (c) 2018, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('Service Level Agreement', {
	setup: function(frm) {
		let allow_statuses = [];
		const exclude_statuses = ['Open', 'Closed', 'Resolved'];

		vmraid.model.with_doctype('Issue', () => {
			let statuses = vmraid.meta.get_docfield('Issue', 'status', frm.doc.name).options;
			statuses = statuses.split('\n');
			allow_statuses = statuses.filter((status) => !exclude_statuses.includes(status));
			frm.fields_dict.pause_sla_on.grid.update_docfield_property(
				'status', 'options', [''].concat(allow_statuses)
			);
		});
	}
});
