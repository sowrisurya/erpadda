QUnit.module('Sales Order');

QUnit.test("test_sales_order_without_bypass_credit_limit_check", function(assert) {
//#PR : 10861, Author : ashish-greycube & jigneshpshah,  Email:mr.ashish.shah@gmail.com
	assert.expect(2);
	let done = assert.async();
	vmraid.run_serially([
		() => vmraid.new_doc('Customer'),
		() => vmraid.timeout(1),
		() => vmraid.quick_entry.dialog.$wrapper.find('.edit-full').click(),
		() => vmraid.timeout(1),
		() => cur_frm.set_value("customer_name", "Test Customer 11"),
		() => cur_frm.add_child('credit_limits', {
			'credit_limit': 1000,
			'company': '_Test Company',
			'bypass_credit_limit_check': 1}),
		// save form
		() => cur_frm.save(),
		() => vmraid.timeout(1),

		() => vmraid.new_doc('Item'),
		() => vmraid.timeout(1),
		() => vmraid.click_link('Edit in full page'),
		() => cur_frm.set_value("item_code", "Test Product 11"),
		() => cur_frm.set_value("item_group", "Products"),
		() => cur_frm.set_value("standard_rate", 100),
		// save form
		() => cur_frm.save(),
		() => vmraid.timeout(1),

		() => {
			return vmraid.tests.make('Sales Order', [
				{customer: 'Test Customer 11'},
				{items: [
					[
						{'delivery_date': vmraid.datetime.add_days(vmraid.defaults.get_default("year_end_date"), 1)},
						{'qty': 5},
						{'item_code': 'Test Product 11'},
					]
				]}

			]);
		},
		() => cur_frm.save(),
		() => vmraid.tests.click_button('Submit'),
		() => assert.equal("Confirm", cur_dialog.title,'confirmation for submit'),
		() => vmraid.tests.click_button('Yes'),
		() => vmraid.timeout(3),
		() => {

			if (cur_dialog.body.innerText.match(/^Credit limit has been crossed for customer.*$/))
				{
    				/*Match found */
    				assert.ok(true, "Credit Limit crossed message received");
				}


		},
		() => cur_dialog.cancel(),
		() => done()
	]);
});
