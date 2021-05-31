QUnit.module('Selling');

QUnit.test("test sales order with margin", function(assert) {
	assert.expect(3);
	let done = assert.async();
	vmraid.run_serially([
		() => {
			return vmraid.tests.make('Sales Order', [
				{customer:'Test Customer 1'},
				{selling_price_list: 'Test-Selling-USD'},
				{currency: 'USD'},
				{items: [
					[
						{'item_code': 'Test Product 4'},
						{'delivery_date': vmraid.datetime.add_days(vmraid.defaults.get_default("year_end_date"), 1)},
						{'qty': 1},
						{'margin_type': 'Amount'},
						{'margin_rate_or_amount': 20}
					]
				]},
			]);
		},

		() => cur_frm.save(),
		() => {
			// get_rate_details
			assert.ok(cur_frm.doc.items[0].rate_with_margin == 220, "Margin rate correct");
			assert.ok(cur_frm.doc.items[0].base_rate_with_margin == cur_frm.doc.conversion_rate * 220, "Base margin rate correct");
			assert.ok(cur_frm.doc.total == 220, "Amount correct");
		},

		() => vmraid.tests.click_button('Submit'),
		() => vmraid.tests.click_button('Yes'),
		() => vmraid.timeout(0.3),
		() => done()
	]);
});

