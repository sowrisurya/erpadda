// Copyright (c) 2019, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('Loan Type', {
	onload: function(frm) {
		$.each(["penalty_income_account", "interest_income_account"], function (i, field) {
			frm.set_query(field, function () {
				return {
					"filters": {
						"company": frm.doc.company,
						"root_type": "Income",
						"is_group": 0
					}
				};
			});
		});

		$.each(["payment_account", "loan_account"], function (i, field) {
			frm.set_query(field, function () {
				return {
					"filters": {
						"company": frm.doc.company,
						"root_type": "Asset",
						"is_group": 0
					}
				};
			});
		});
	}
});
