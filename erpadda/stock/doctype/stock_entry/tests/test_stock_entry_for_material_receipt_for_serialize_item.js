QUnit.module('Stock');

QUnit.test("test material receipt", function(assert) {
	assert.expect(2);
	let done = assert.async();
	vmraid.run_serially([
		() => {
			return vmraid.tests.make('Stock Entry', [
				{purpose:'Material Receipt'},
				{to_warehouse:'Stores - '+vmraid.get_abbr(vmraid.defaults.get_default('Company'))},
				{items: [
					[
						{'item_code': 'Test Product 4'},
						{'qty': 5},
						{'batch_no':'TEST-BATCH-001'},
						{'serial_no':'Test-Product-001\nTest-Product-002\nTest-Product-003\nTest-Product-004\nTest-Product-005'},
						{'basic_rate':100},
					]
				]},
			]);
		},
		() => cur_frm.save(),
		() => vmraid.click_button('Update Rate and Availability'),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.items[0].item_name=='Test Product 4', "Item name correct");
			assert.ok(cur_frm.doc.total_incoming_value==500, " Incoming Value correct");
		},
		() => vmraid.tests.click_button('Submit'),
		() => vmraid.tests.click_button('Yes'),
		() => vmraid.timeout(0.3),
		() => done()
	]);
});

