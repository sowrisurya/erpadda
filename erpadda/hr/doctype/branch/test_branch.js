QUnit.module('hr');

QUnit.test("Test: Branch [HR]", function (assert) {
	assert.expect(1);
	let done = assert.async();

	vmraid.run_serially([
		// test branch creation
		() => vmraid.set_route("List", "Branch", "List"),
		() => vmraid.new_doc("Branch"),
		() => vmraid.timeout(1),
		() => vmraid.quick_entry.dialog.$wrapper.find('.edit-full').click(),
		() => vmraid.timeout(1),
		() => cur_frm.set_value("branch", "Test Branch"),

		// save form
		() => cur_frm.save(),
		() => vmraid.timeout(1),
		() => assert.equal("Test Branch", cur_frm.doc.branch,
			'name of branch correctly saved'),
		() => done()
	]);
});