// Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

cur_frm.add_fetch("customer", "customer_group", "customer_group" );
cur_frm.add_fetch("supplier", "supplier_group_name", "supplier_group" );

vmraid.ui.form.on("Tax Rule", "tax_type", function(frm) {
	frm.toggle_reqd("sales_tax_template", frm.doc.tax_type=="Sales");
	frm.toggle_reqd("purchase_tax_template", frm.doc.tax_type=="Purchase");
})

vmraid.ui.form.on("Tax Rule", "onload", function(frm) {
	if(frm.doc.__islocal) {
		frm.set_value("use_for_shopping_cart", 1);
	}
})

vmraid.ui.form.on("Tax Rule", "refresh", function(frm) {
	vmraid.ui.form.trigger("Tax Rule", "tax_type");
})

vmraid.ui.form.on("Tax Rule", "customer", function(frm) {
	if(frm.doc.customer) {
		vmraid.call({
			method:"erpadda.accounts.doctype.tax_rule.tax_rule.get_party_details",
			args: {
				"party": frm.doc.customer,
				"party_type": "customer"
			},
			callback: function(r) {
				if(!r.exc) {
					$.each(r.message, function(k, v) {
						frm.set_value(k, v);
					});
				}
			}
		});
	}
});

vmraid.ui.form.on("Tax Rule", "supplier", function(frm) {
	if(frm.doc.supplier) {
		vmraid.call({
			method:"erpadda.accounts.doctype.tax_rule.tax_rule.get_party_details",
			args: {
				"party": frm.doc.supplier,
				"party_type": "supplier"
			},
			callback: function(r) {
				if(!r.exc) {
					$.each(r.message, function(k, v) {
						frm.set_value(k, v);
					});
				}
			}
		});
	}
});
