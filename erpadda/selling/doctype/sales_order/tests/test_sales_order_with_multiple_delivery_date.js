/* eslint-disable */
// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Sales Order", function (assert) {
	assert.expect(2);
	let done = assert.async();
	let delivery_date = vmraid.datetime.add_days(vmraid.defaults.get_default("year_end_date"), 1);

	vmraid.run_serially([
		// insert a new Sales Order
		() => {
			return vmraid.tests.make('Sales Order', [
				{customer: "Test Customer 1"},
				{delivery_date: delivery_date},
				{order_type: 'Sales'},
				{items: [
					[
						{"item_code": "Test Product 1"},
						{"qty": 5},
						{'rate': 100},
					]]
				}
			])
		},
		() => {
			assert.ok(cur_frm.doc.items[0].delivery_date == delivery_date);
		},
		() => vmraid.timeout(1),
		// make SO without delivery date in parent,
		// parent delivery date should be set based on final delivery date entered in item
		() => {
			return vmraid.tests.make('Sales Order', [
				{customer: "Test Customer 1"},
				{order_type: 'Sales'},
				{items: [
					[
						{"item_code": "Test Product 1"},
						{"qty": 5},
						{'rate': 100},
						{'delivery_date': delivery_date}
					],
					[
						{"item_code": "Test Product 2"},
						{"qty": 5},
						{'rate': 100},
						{'delivery_date': vmraid.datetime.add_days(delivery_date, 5)}
					]]
				}
			])
		},
		() => cur_frm.save(),
		() => vmraid.timeout(1),
		() => {
			assert.ok(cur_frm.doc.delivery_date == vmraid.datetime.add_days(delivery_date, 5));
		},
		() => done()
	]);
});