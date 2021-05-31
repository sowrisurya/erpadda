QUnit.module('Buying');

QUnit.test("test: purchase order with multi UOM", function(assert) {
	assert.expect(3);
	let done = assert.async();

	vmraid.run_serially([
		() => {
			return vmraid.tests.make('Purchase Order', [
				{supplier: 'Test Supplier'},
				{is_subcontracted: 'No'},
				{items: [
					[
						{"item_code": 'Test Product 4'},
						{"qty": 5},
						{"uom": 'Unit'},
						{"rate": 100},
						{"schedule_date": vmraid.datetime.add_days(vmraid.datetime.now_date(), 1)},
						{"expected_delivery_date": vmraid.datetime.add_days(vmraid.datetime.now_date(), 5)},
						{"warehouse": 'Stores - '+vmraid.get_abbr(vmraid.defaults.get_default("Company"))}
					]
				]}
			]);
		},

		() => {
			assert.ok(cur_frm.doc.supplier_name == 'Test Supplier', "Supplier name correct");
			assert.ok(cur_frm.doc.items[0].item_name == 'Test Product 4', "Item name correct");
			assert.ok(cur_frm.doc.items[0].uom == 'Unit', "Multi UOM correct");
		},

		() => vmraid.timeout(1),
		() => vmraid.tests.click_button('Submit'),
		() => vmraid.tests.click_button('Yes'),
		() => vmraid.timeout(0.3),

		() => done()
	]);
});