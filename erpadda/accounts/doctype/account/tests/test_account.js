QUnit.module('accounts');

QUnit.test("test account", function(assert) {
	assert.expect(4);
	let done = assert.async();
	vmraid.run_serially([
		() => vmraid.set_route('Tree', 'Account'),
		() => vmraid.timeout(3),
		() => vmraid.click_button('Expand All'),
		() => vmraid.timeout(1),
		() => vmraid.click_link('Debtors'),
		() => vmraid.click_button('Edit'),
		() => vmraid.timeout(1),
		() => {
			assert.ok(cur_frm.doc.root_type=='Asset');
			assert.ok(cur_frm.doc.report_type=='Balance Sheet');
			assert.ok(cur_frm.doc.account_type=='Receivable');
		},
		() => vmraid.click_button('Ledger'),
		() => vmraid.timeout(1),
		() => {
			// check if general ledger report shown
			assert.deepEqual(vmraid.get_route(), ['query-report', 'General Ledger']);
			window.history.back();
			return vmraid.timeout(1);
		},
		() => done()
	]);
});
