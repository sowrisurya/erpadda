// Copyright (c) 2016, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('Shopify Log', {
	refresh: function(frm) {
		if (frm.doc.request_data && frm.doc.status=='Error'){
			frm.add_custom_button('Resync', function() {
				vmraid.call({
					method:"erpadda.erpadda_integrations.doctype.shopify_log.shopify_log.resync",
					args:{
						method:frm.doc.method,
						name: frm.doc.name,
						request_data: frm.doc.request_data
					},
					callback: function(r){
						vmraid.msgprint(__("Order rescheduled for sync"))
					}
				})
			}).addClass('btn-primary');
		}
	}
});
