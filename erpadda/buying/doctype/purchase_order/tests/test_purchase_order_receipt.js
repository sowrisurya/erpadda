QUnit.module('Buying');

QUnit.test("test: purchase order receipt", function(assert) {
	assert.expect(5);
	let done = assert.async();

	vmraid.run_serially([
		() => {
			return vmraid.tests.make('Purchase Order', [
				{supplier: 'Test Supplier'},
				{is_subcontracted: 'No'},
				{buying_price_list: 'Test-Buying-USD'},
				{currency: 'USD'},
				{items: [
					[
						{"item_code": 'Test Product 1'},
						{"schedule_date": vmraid.datetime.add_days(vmraid.datetime.now_date(), 1)},
						{"expected_delivery_date": vmraid.datetime.add_days(vmraid.datetime.now_date(), 5)},
						{"qty": 5},
						{"uom": 'Unit'},
						{"rate": 100},
						{"warehouse": 'Stores - '+vmraid.get_abbr(vmraid.defaults.get_default("Company"))}
					]
				]},
			]);
		},

		() => {

			// Check supplier and item details
			assert.ok(cur_frm.doc.supplier_name == 'Test Supplier', "Supplier name correct");
			assert.ok(cur_frm.doc.items[0].item_name == 'Test Product 1', "Item name correct");
			assert.ok(cur_frm.doc.items[0].description == 'Test Product 1', "Description correct");
			assert.ok(cur_frm.doc.items[0].qty == 5, "Quantity correct");

		},

		() => vmraid.timeout(1),

		() => vmraid.tests.click_button('Submit'),
		() => vmraid.tests.click_button('Yes'),

		() => vmraid.timeout(1.5),
		() => vmraid.click_button('Close'),
		() => vmraid.timeout(0.3),

		// Make Purchase Receipt
		() => vmraid.click_button('Make'),
		() => vmraid.timeout(0.3),

		() => vmraid.click_link('Receipt'),
		() => vmraid.timeout(2),

		() => cur_frm.save(),

		// Save and submit Purchase Receipt
		() => vmraid.timeout(1),
		() => vmraid.tests.click_button('Submit'),
		() => vmraid.tests.click_button('Yes'),
		() => vmraid.timeout(1),

		// View Purchase order in Stock Ledger
		() => vmraid.click_button('View'),
		() => vmraid.timeout(0.3),

		() => vmraid.click_link('Stock Ledger'),
		() => vmraid.timeout(2),
		() => {
			assert.ok($('div.slick-cell.l2.r2 > a').text().includes('Test Product 1')
				&& $('div.slick-cell.l9.r9 > div').text().includes(5), "Stock ledger entry correct");
		},
		() => done()
	]);
});
