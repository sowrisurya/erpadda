/* eslint-disable */
// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Restaurant Order Entry", function (assert) {
	let done = assert.async();

	// number of asserts
	assert.expect(5);

	vmraid.run_serially([
		// insert a new Restaurant Order Entry
		() => vmraid.set_route('Form', 'Restaurant Settings'),
		() => cur_frm.set_value('default_customer', 'Test Customer 1'),
		() => cur_frm.save(),
		() => vmraid.set_route('Form', 'Restaurant Order Entry'),
		() => vmraid.click_button('Clear'),
		() => vmraid.timeout(2),
		() => cur_frm.set_value('restaurant_table', 'Test-Restaurant-1-01'),
		() => cur_frm.set_value('add_item', 'Food Item 1'),
		() => vmraid.timeout(0.5),
		() => {
			var e = $.Event( "keyup", {which: 13} );
			$('input[data-fieldname="add_item"]').trigger(e);
			return vmraid.timeout(0.5);
		},
		() => cur_frm.set_value('add_item', 'Food Item 1'),
		() => {
			var e = $.Event( "keyup", {which: 13} );
			$('input[data-fieldname="add_item"]').trigger(e);
			return vmraid.timeout(0.5);
		},
		() => cur_frm.set_value('add_item', 'Food Item 2'),
		() => {
			var e = $.Event( "keyup", {which: 13} );
			$('input[data-fieldname="add_item"]').trigger(e);
			return vmraid.timeout(0.5);
		},
		() => {
			assert.equal(cur_frm.doc.items[0].item, 'Food Item 1');
			assert.equal(cur_frm.doc.items[0].qty, 2);
			assert.equal(cur_frm.doc.items[1].item, 'Food Item 2');
			assert.equal(cur_frm.doc.items[1].qty, 1);
		},
		() => vmraid.click_button('Update'),
		() => vmraid.timeout(2),
		() => {
			assert.equal(cur_frm.doc.grand_total, 290);
		}
		() => done()
	]);

});
