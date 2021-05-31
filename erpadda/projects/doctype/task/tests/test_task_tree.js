/* eslint-disable */
// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Task Tree", function (assert) {
	let done = assert.async();

	// number of asserts
	assert.expect(4);

	vmraid.run_serially([
		// insert a new Task
		() => vmraid.set_route('Tree', 'Task'),
		() => vmraid.timeout(0.5),

		// Checking adding child without selecting any Node
		() => vmraid.tests.click_button('New'),
		() => vmraid.timeout(0.5),
		() => {assert.equal($(`.msgprint`).text(), "Select a group node first.", "Error message success");},
		() => vmraid.tests.click_button('Close'),
		() => vmraid.timeout(0.5),

		// Creating child nodes
		() => vmraid.tests.click_link('All Tasks'),
		() => vmraid.map_group.make('Test-1'),
		() => vmraid.map_group.make('Test-3', 1),
		() => vmraid.timeout(1),
		() => vmraid.tests.click_link('Test-3'),
		() => vmraid.map_group.make('Test-4', 0),

		// Checking Edit button
		() => vmraid.timeout(0.5),
		() => vmraid.tests.click_link('Test-1'),
		() => vmraid.tests.click_button('Edit'),
		() => vmraid.timeout(1),
		() => vmraid.db.get_value('Task', {'subject': 'Test-1'}, 'name'),
		(task) => {assert.deepEqual(vmraid.get_route(), ["Form", "Task", task.message.name], "Edit route checks");},

		// Deleting child Node
		() => vmraid.set_route('Tree', 'Task'),
		() => vmraid.timeout(0.5),
		() => vmraid.tests.click_link('Test-1'),
		() => vmraid.tests.click_button('Delete'),
		() => vmraid.timeout(0.5),
		() => vmraid.tests.click_button('Yes'),

		// Deleting Group Node that has child nodes in it
		() => vmraid.timeout(0.5),
		() => vmraid.tests.click_link('Test-3'),
		() => vmraid.tests.click_button('Delete'),
		() => vmraid.timeout(0.5),
		() => vmraid.tests.click_button('Yes'),
		() => vmraid.timeout(1),
		() => {assert.equal(cur_dialog.title, 'Message', 'Error thrown correctly');},
		() => vmraid.tests.click_button('Close'),

		// Add multiple child tasks
		() => vmraid.tests.click_link('Test-3'),
		() => vmraid.timeout(0.5),
		() => vmraid.click_button('Add Multiple'),
		() => vmraid.timeout(1),
		() => cur_dialog.set_value('tasks', 'Test-6\nTest-7'),
		() => vmraid.timeout(0.5),
		() => vmraid.click_button('Submit'),
		() => vmraid.timeout(2),
		() => vmraid.click_button('Expand All'),
		() => vmraid.timeout(1),
		() => {
			let count = $(`a:contains("Test-6"):visible`).length + $(`a:contains("Test-7"):visible`).length;
			assert.equal(count, 2, "Multiple Tasks added successfully");
		},

		() => done()
	]);
});

vmraid.map_group = {
	make:function(subject, is_group = 0){
		return vmraid.run_serially([
			() => vmraid.click_button('Add Child'),
			() => vmraid.timeout(1),
			() => cur_dialog.set_value('is_group', is_group),
			() => cur_dialog.set_value('subject', subject),
			() => vmraid.click_button('Create New'),
			() => vmraid.timeout(1.5)
		]);
	}
};
