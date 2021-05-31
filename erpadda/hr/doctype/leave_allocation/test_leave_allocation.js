QUnit.module('hr');

QUnit.test("Test: Leave allocation [HR]", function (assert) {
	assert.expect(3);
	let done = assert.async();
	let today_date = vmraid.datetime.nowdate();

	vmraid.run_serially([
		// test creating leave alloction
		() => vmraid.set_route("List", "Leave Allocation", "List"),
		() => vmraid.new_doc("Leave Allocation"),
		() => vmraid.timeout(1),
		() => {
			vmraid.db.get_value('Employee', {'employee_name':'Test Employee 1'}, 'name', function(r) {
				cur_frm.set_value("employee", r.name)
			});
		},
		() => vmraid.timeout(1),
		() => cur_frm.set_value("leave_type", "Test Leave type"),
		() => cur_frm.set_value("to_date", vmraid.datetime.add_months(today_date, 2)),	// for two months
		() => cur_frm.set_value("description", "This is just for testing"),
		() => cur_frm.set_value("new_leaves_allocated", 2),
		() => vmraid.click_check('Add unused leaves from previous allocations'),
		// save form
		() => cur_frm.save(),
		() => vmraid.timeout(1),
		() => cur_frm.savesubmit(),
		() => vmraid.timeout(1),
		() => assert.equal("Confirm", cur_dialog.title,
			'confirmation for leave alloction shown'),
		() => vmraid.click_button('Yes'),
		() => vmraid.timeout(1),
		// check auto filled from date
		() => assert.equal(today_date, cur_frm.doc.from_date,
			"from date correctly set"),
		// check for total leaves
		() => assert.equal(cur_frm.doc.unused_leaves + 2, cur_frm.doc.total_leaves_allocated,
			"total leave calculation is correctly set"),
		() => done()
	]);
});