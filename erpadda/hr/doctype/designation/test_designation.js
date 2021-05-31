QUnit.module('hr');

QUnit.test("Test: Designation [HR]", function (assert) {
	assert.expect(1);
	let done = assert.async();

	vmraid.run_serially([
		// test designation creation
		() => vmraid.set_route("List", "Designation", "List"),
		() => vmraid.new_doc("Designation"),
		() => vmraid.timeout(1),
		() => vmraid.quick_entry.dialog.$wrapper.find('.edit-full').click(),
		() => vmraid.timeout(1),
		() => cur_frm.set_value("designation_name", "Test Designation"),
		() => cur_frm.set_value("description", "This designation is just for testing."),
		// save form
		() => cur_frm.save(),
		() => vmraid.timeout(1),
		() => assert.equal("Test Designation", cur_frm.doc.designation_name,
			'name of designation correctly saved'),
		() => done()
	]);
});