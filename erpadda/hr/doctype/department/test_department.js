QUnit.module('hr');

QUnit.test("Test: Department [HR]", function (assert) {
	assert.expect(1);
	let done = assert.async();

	vmraid.run_serially([
		// test department creation
		() => vmraid.set_route("List", "Department", "List"),
		() => vmraid.new_doc("Department"),
		() => vmraid.timeout(1),
		() => vmraid.quick_entry.dialog.$wrapper.find('.edit-full').click(),
		() => vmraid.timeout(1),
		() => cur_frm.set_value("department_name", "Test Department"),
		() => cur_frm.set_value("leave_block_list", "Test Leave block list"),
		// save form
		() => cur_frm.save(),
		() => vmraid.timeout(1),
		() => assert.equal("Test Department", cur_frm.doc.department_name,
			'name of department correctly saved'),
		() => done()
	]);
});