// Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('Fertilizer', {
	onload: (frm) => {
		if (frm.doc.fertilizer_contents == undefined) frm.call('load_contents');
	}
});
