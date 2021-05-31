QUnit.module('hr');

QUnit.test("Test: Employment type [HR]", function (assert) {
	assert.expect(1);
	let done = assert.async();

	vmraid.run_serially([
		// test employment type creation
		() => vmraid.set_route("List", "Employment Type", "List"),
		() => vmraid.new_doc("Employment Type"),
		() => vmraid.timeout(1),
		() => vmraid.quick_entry.dialog.$wrapper.find('.edit-full').click(),
		() => vmraid.timeout(1),
		() => cur_frm.set_value("employee_type_name", "Test Employment type"),
		// save form
		() => cur_frm.save(),
		() => vmraid.timeout(1),
		() => assert.equal("Test Employment type", cur_frm.doc.employee_type_name,
			'name of employment type correctly saved'),
		() => done()
	]);
});