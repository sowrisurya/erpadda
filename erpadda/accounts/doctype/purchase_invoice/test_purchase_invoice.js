QUnit.module('Purchase Invoice');

QUnit.test("test purchase invoice", function(assert) {
	assert.expect(9);
	let done = assert.async();
	vmraid.run_serially([
		() => {
			return vmraid.tests.make('Purchase Invoice', [
				{supplier: 'Test Supplier'},
				{bill_no: 'in123'},
				{items: [
					[
						{'qty': 5},
						{'item_code': 'Test Product 1'},
						{'rate':100},
					]
				]},
				{update_stock:1},
				{supplier_address: 'Test1-Billing'},
				{contact_person: 'Contact 3-Test Supplier'},
				{taxes_and_charges: 'TEST In State GST - FT'},
				{tc_name: 'Test Term 1'},
				{terms: 'This is Test'},
				{payment_terms_template: '_Test Payment Term Template UI'}
			]);
		},
		() => cur_frm.save(),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.items[0].item_name=='Test Product 1', "Item name correct");
			// get tax details
			assert.ok(cur_frm.doc.taxes_and_charges=='TEST In State GST - FT', "Tax details correct");
			// get tax account head details
			assert.ok(cur_frm.doc.taxes[0].account_head=='CGST - '+vmraid.get_abbr(vmraid.defaults.get_default('Company')), " Account Head abbr correct");
			// grand_total Calculated
			assert.ok(cur_frm.doc.grand_total==590, "Grad Total correct");

			assert.ok(cur_frm.doc.payment_terms_template, "Payment Terms Template is correct");
			assert.ok(cur_frm.doc.payment_schedule.length > 0, "Payment Term Schedule is not empty");

		},
		() => {
			let date = cur_frm.doc.due_date;
			vmraid.tests.set_control('due_date', vmraid.datetime.add_days(date, 1));
			vmraid.timeout(0.5);
			assert.ok(cur_dialog && cur_dialog.is_visible, 'Message is displayed to user');
		},
		() => vmraid.timeout(1),
		() => vmraid.tests.click_button('Close'),
		() => vmraid.timeout(0.5),
		() => vmraid.tests.set_form_values(cur_frm, [{'payment_terms_schedule': ''}]),
		() => {
			let date = cur_frm.doc.due_date;
			vmraid.tests.set_control('due_date', vmraid.datetime.add_days(date, 1));
			vmraid.timeout(0.5);
			assert.ok(cur_dialog && cur_dialog.is_visible, 'Message is displayed to user');
		},
		() => vmraid.timeout(1),
		() => vmraid.tests.click_button('Close'),
		() => vmraid.timeout(0.5),
		() => vmraid.tests.set_form_values(cur_frm, [{'payment_schedule': []}]),
		() => {
			let date = cur_frm.doc.due_date;
			vmraid.tests.set_control('due_date', vmraid.datetime.add_days(date, 1));
			vmraid.timeout(0.5);
			assert.ok(!cur_dialog, 'Message is not shown');
		},
		() => cur_frm.save(),
		() => vmraid.tests.click_button('Submit'),
		() => vmraid.tests.click_button('Yes'),
		() => vmraid.timeout(1),
		() => done()
	]);
});

