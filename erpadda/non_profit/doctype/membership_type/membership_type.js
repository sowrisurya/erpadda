// Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('Membership Type', {
	refresh: function (frm) {
		vmraid.db.get_single_value('Non Profit Settings', 'enable_razorpay_for_memberships').then(val => {
			if (val) frm.set_df_property('razorpay_plan_id', 'hidden', false);
		});

		vmraid.db.get_single_value('Non Profit Settings', 'allow_invoicing').then(val => {
			if (val) frm.set_df_property('linked_item', 'hidden', false);
		});

		frm.set_query('linked_item', () => {
			return {
				filters: {
					is_stock_item: 0
				}
			};
		});
	}
});
