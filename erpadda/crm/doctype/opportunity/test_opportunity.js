QUnit.test("test: opportunity", function (assert) {
	assert.expect(8);
	let done = assert.async();
	vmraid.run_serially([
		() => vmraid.set_route('List', 'Opportunity'),
		() => vmraid.timeout(1),
		() => vmraid.click_button('New'),
		() => vmraid.timeout(1),
		() => cur_frm.set_value('opportunity_from', 'Customer'),
		() => cur_frm.set_value('customer', 'Test Customer 1'),

		// check items
		() => cur_frm.set_value('with_items', 1),
		() => vmraid.tests.set_grid_values(cur_frm, 'items', [
			[
				{item_code:'Test Product 1'},
				{qty: 4}
			]
		]),
		() => cur_frm.save(),
		() => vmraid.timeout(1),
		() => {
			assert.notOk(cur_frm.is_new(), 'saved');
			vmraid.opportunity_name = cur_frm.doc.name;
		},

		// close and re-open
		() => vmraid.click_button('Close'),
		() => vmraid.timeout(1),
		() => assert.equal(cur_frm.doc.status, 'Closed',
			'closed'),

		() => vmraid.click_button('Reopen'),
		() => assert.equal(cur_frm.doc.status, 'Open',
			'reopened'),
		() => vmraid.timeout(1),

		// make quotation
		() => vmraid.click_button('Make'),
		() => vmraid.click_link('Quotation', 1),
		() => vmraid.timeout(2),
		() => {
			assert.equal(vmraid.get_route()[1], 'Quotation',
				'made quotation');
			assert.equal(cur_frm.doc.customer, 'Test Customer 1',
				'customer set in quotation');
			assert.equal(cur_frm.doc.items[0].item_code, 'Test Product 1',
				'item set in quotation');
			assert.equal(cur_frm.doc.items[0].qty, 4,
				'qty set in quotation');
			assert.equal(cur_frm.doc.items[0].prevdoc_docname, vmraid.opportunity_name,
				'opportunity set in quotation');
		},
		() => done()
	]);
});
