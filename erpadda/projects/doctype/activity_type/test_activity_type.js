QUnit.test("test: Activity Type", function (assert) {
	// number of asserts
	assert.expect(1);
	let done = assert.async();

	vmraid.run_serially([
		// insert a new Activity Type
		() => vmraid.set_route("List", "Activity Type", "List"),
		() => vmraid.new_doc("Activity Type"),
		() => vmraid.timeout(1),
		() => vmraid.quick_entry.dialog.$wrapper.find('.edit-full').click(),
		() => vmraid.timeout(1),
		() => cur_frm.set_value("activity_type", "Test Activity"),
		() => vmraid.click_button('Save'),
		() => vmraid.timeout(1),
		() => {
			assert.equal(cur_frm.doc.name,"Test Activity");
		},
		() => done()
	]);
});
