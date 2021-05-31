QUnit.module('Buying');

QUnit.test("test: purchase order with get items", function(assert) {
	assert.expect(4);
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
						{"item_code": 'Test Product 4'},
						{"qty": 5},
						{"schedule_date": vmraid.datetime.add_days(vmraid.datetime.now_date(), 1)},
						{"expected_delivery_date": vmraid.datetime.add_days(vmraid.datetime.now_date(), 5)},
						{"warehouse": 'Stores - '+vmraid.get_abbr(vmraid.defaults.get_default("Company"))}
					]
				]}
			]);
		},

		() => {
			assert.ok(cur_frm.doc.supplier_name == 'Test Supplier', "Supplier name correct");
		},

		() => vmraid.timeout(0.3),
		() => vmraid.click_button('Get items from'),
		() => vmraid.timeout(0.3),

		() => vmraid.click_link('Product Bundle'),
		() => vmraid.timeout(0.5),

		() => cur_dialog.set_value('product_bundle', 'Computer'),
		() => vmraid.click_button('Get Items'),
		() => vmraid.timeout(1),

		// Check if items are fetched from Product Bundle
		() => {
			assert.ok(cur_frm.doc.items[1].item_name == 'CPU', "Product bundle item 1 correct");
			assert.ok(cur_frm.doc.items[2].item_name == 'Screen', "Product bundle item 2 correct");
			assert.ok(cur_frm.doc.items[3].item_name == 'Keyboard', "Product bundle item 3 correct");
		},

		() => cur_frm.doc.items[1].warehouse = 'Stores - '+vmraid.get_abbr(vmraid.defaults.get_default("Company")),
		() => cur_frm.doc.items[2].warehouse = 'Stores - '+vmraid.get_abbr(vmraid.defaults.get_default("Company")),
		() => cur_frm.doc.items[3].warehouse = 'Stores - '+vmraid.get_abbr(vmraid.defaults.get_default("Company")),

		() => cur_frm.save(),
		() => vmraid.timeout(1),

		() => vmraid.tests.click_button('Submit'),
		() => vmraid.tests.click_button('Yes'),
		() => vmraid.timeout(0.3),

		() => done()
	]);
});