// Copyright (c) 2020, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('POS Invoice Merge Log', {
	setup: function(frm) {
		frm.set_query("pos_invoice", "pos_invoices", doc => {
			return{
				filters: { 
					'docstatus': 1,
					'customer': doc.customer, 
					'consolidated_invoice': '' 
				}
			}
		});
	}
});