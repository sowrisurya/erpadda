QUnit.module('Quotation');

QUnit.test("test quotation submit cancel amend", function(assert) {
	assert.expect(2);
	let done = assert.async();
	vmraid.run_serially([
		() => {
			return vmraid.tests.make('Quotation', [
				{customer: 'Test Customer 1'},
				{items: [
					[
						{'delivery_date': vmraid.datetime.add_days(vmraid.defaults.get_default("year_end_date"), 1)},
						{'qty': 5},
						{'item_code': 'Test Product 1'}
					]
				]},
				{customer_address: 'Test1-Billing'},
				{shipping_address_name: 'Test1-Shipping'},
				{contact_person: 'Contact 1-Test Customer 1'}
			]);
		},
		() => cur_frm.save(),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.items[0].item_name=='Test Product 1', "Item name correct");
			// get uom details
			assert.ok(cur_frm.doc.grand_total== 500, "Grand total correct ");

		},
		() => vmraid.tests.click_button('Submit'),
		() => vmraid.tests.click_button('Yes'),
		() => vmraid.timeout(1),
		() => vmraid.tests.click_button('Close'),
		() => vmraid.tests.click_button('Cancel'),
		() => vmraid.tests.click_button('Yes'),
		() => vmraid.timeout(0.5),
		() => vmraid.tests.click_button('Amend'),
		() => cur_frm.save(),
		() => done()
	]);
});
