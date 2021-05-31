QUnit.module('Payment Entry');

QUnit.test("test payment entry", function(assert) {
	assert.expect(6);
	let done = assert.async();
	vmraid.run_serially([
		() => {
			return vmraid.tests.make('Sales Invoice', [
				{customer: 'Test Customer 1'},
				{items: [
					[
						{'item_code': 'Test Product 1'},
						{'qty': 1},
						{'rate': 101},
					]
				]}
			]);
		},
		() => cur_frm.save(),
		() => vmraid.tests.click_button('Submit'),
		() => vmraid.tests.click_button('Yes'),
		() => vmraid.timeout(1),
		() => vmraid.tests.click_button('Close'),
		() => vmraid.timeout(1),
		() => vmraid.click_button('Make'),
		() => vmraid.timeout(1),
		() => vmraid.click_link('Payment'),
		() => vmraid.timeout(2),
		() => {
			assert.equal(vmraid.get_route()[1], 'Payment Entry',
				'made payment entry');
			assert.equal(cur_frm.doc.party, 'Test Customer 1',
				'customer set in payment entry');
			assert.equal(cur_frm.doc.paid_amount, 101,
				'paid amount set in payment entry');
			assert.equal(cur_frm.doc.references[0].allocated_amount, 101,
				'amount allocated against sales invoice');
		},
		() => vmraid.timeout(1),
		() => cur_frm.set_value('paid_amount', 100),
		() => vmraid.timeout(1),
		() => {
			vmraid.model.set_value("Payment Entry Reference", cur_frm.doc.references[0].name,
				"allocated_amount", 101);
		},
		() => vmraid.timeout(1),
		() => vmraid.click_button('Write Off Difference Amount'),
		() => vmraid.timeout(1),
		() => {
			assert.equal(cur_frm.doc.difference_amount, 0, 'difference amount is zero');
			assert.equal(cur_frm.doc.deductions[0].amount, 1, 'Write off amount = 1');
		},
		() => done()
	]);
});
