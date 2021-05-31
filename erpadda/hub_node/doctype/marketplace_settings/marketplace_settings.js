// Copyright (c) 2018, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('Marketplace Settings', {
	refresh: function(frm) {
		$('#toolbar-user .marketplace-link').toggle(!frm.doc.disable_marketplace);
	},
});
