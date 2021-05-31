QUnit.module('Stock');

QUnit.test("test material request for transfer", function(assert) {
	assert.expect(1);
	let done = assert.async();
	vmraid.run_serially([
		() => {
			return vmraid.tests.make('Material Request', [
				{material_request_type:'Manufacture'},
				{items: [
					[
						{'schedule_date':  vmraid.datetime.add_days(vmraid.datetime.nowdate(), 5)},
						{'qty': 5},
						{'item_code': 'Test Product 1'},
					]
				]},
			]);
		},
		() => cur_frm.save(),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.items[0].item_name=='Test Product 1', "Item name correct");
		},
		() => vmraid.tests.click_button('Submit'),
		() => vmraid.tests.click_button('Yes'),
		() => vmraid.timeout(0.3),
		() => done()
	]);
});

