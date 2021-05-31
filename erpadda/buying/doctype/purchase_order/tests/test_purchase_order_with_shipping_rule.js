QUnit.module('Buying');

QUnit.test("test: purchase order with shipping rule", function(assert) {
	assert.expect(3);
	let done = assert.async();

	vmraid.run_serially([
		() => {
			return vmraid.tests.make('Purchase Order', [
				{supplier: 'Test Supplier'},
				{is_subcontracted: 'No'},
				{buying_price_list: 'Test-Buying-USD'},
				{currency: 'USD'},
				{"schedule_date": vmraid.datetime.add_days(vmraid.datetime.now_date(), 1)},
				{items: [
					[
						{"item_code": 'Test Product 4'},
						{"qty": 5},
						{"uom": 'Unit'},
						{"rate": 500 },
						{"schedule_date": vmraid.datetime.add_days(vmraid.datetime.now_date(), 1)},
						{"expected_delivery_date": vmraid.datetime.add_days(vmraid.datetime.now_date(), 5)},
						{"warehouse": 'Stores - '+vmraid.get_abbr(vmraid.defaults.get_default("Company"))}
					]
				]},

				{shipping_rule:'Two Day Shipping'}
			]);
		},

		() => {
			// Check grand total
			assert.ok(cur_frm.doc.total_taxes_and_charges == 200, "Taxes and charges correct");
			assert.ok(cur_frm.doc.grand_total == 2700, "Grand total correct");
		},

		() => vmraid.timeout(0.3),
		() => vmraid.tests.click_button('Submit'),
		() => vmraid.tests.click_button('Yes'),
		() => vmraid.timeout(0.3),
		() => done()
	]);
});