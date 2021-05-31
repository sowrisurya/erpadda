QUnit.module('Accounts');

QUnit.test("test payment entry", function(assert) {
	assert.expect(1);
	let done = assert.async();
	vmraid.run_serially([
		() => {
			return vmraid.tests.make('Payment Entry', [
				{payment_type:'Receive'},
				{mode_of_payment:'Cash'},
				{party_type:'Customer'},
				{party:'Test Customer 3'},
				{paid_amount:675},
				{reference_no:123},
				{reference_date: vmraid.datetime.add_days(vmraid.datetime.nowdate(), 0)},
			]);
		},
		() => cur_frm.save(),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.total_allocated_amount==675, "Allocated AmountCorrect");
		},
		() => vmraid.tests.click_button('Submit'),
		() => vmraid.tests.click_button('Yes'),
		() => vmraid.timeout(0.3),
		() => done()
	]);
});