// Education Assessment module
QUnit.module('education');

QUnit.test('Test: Assessment Group', function(assert){
	assert.expect(4);
	let done = assert.async();

	vmraid.run_serially([
		() => vmraid.set_route('Tree', 'Assessment Group'),

		// Checking adding child without selecting any Node
		() => vmraid.tests.click_button('New'),
		() => vmraid.timeout(0.2),
		() => {assert.equal($(`.msgprint`).text(), "Select a group node first.", "Error message success");},
		() => vmraid.tests.click_button('Close'),
		() => vmraid.timeout(0.2),

		// Creating child nodes
		() => vmraid.tests.click_link('All Assessment Groups'),
		() => vmraid.map_group.make('Assessment-group-1'),
		() => vmraid.map_group.make('Assessment-group-4', "All Assessment Groups", 1),
		() => vmraid.tests.click_link('Assessment-group-4'),
		() => vmraid.map_group.make('Assessment-group-5', "Assessment-group-3", 0),

		// Checking Edit button
		() => vmraid.timeout(0.5),
		() => vmraid.tests.click_link('Assessment-group-1'),
		() => vmraid.tests.click_button('Edit'),
		() => vmraid.timeout(0.5),
		() => {assert.deepEqual(vmraid.get_route(), ["Form", "Assessment Group", "Assessment-group-1"], "Edit route checks");},

		// Deleting child Node
		() => vmraid.set_route('Tree', 'Assessment Group'),
		() => vmraid.timeout(0.5),
		() => vmraid.tests.click_link('Assessment-group-1'),
		() => vmraid.tests.click_button('Delete'),
		() => vmraid.timeout(0.5),
		() => vmraid.tests.click_button('Yes'),

		// Checking Collapse and Expand button
		() => vmraid.timeout(2),
		() => vmraid.tests.click_link('Assessment-group-4'),
		() => vmraid.click_button('Collapse'),
		() => vmraid.tests.click_link('All Assessment Groups'),
		() => vmraid.click_button('Collapse'),
		() => {assert.ok($('.opened').size() == 0, 'Collapsed');},
		() => vmraid.click_button('Expand'),
		() => {assert.ok($('.opened').size() > 0, 'Expanded');},

		() => done()
	]);
});

vmraid.map_group = {
	make:function(assessment_group_name, parent_assessment_group = 'All Assessment Groups', is_group = 0){
		return vmraid.run_serially([
			() => vmraid.click_button('Add Child'),
			() => vmraid.timeout(0.2),
			() => cur_dialog.set_value('is_group', is_group),
			() => cur_dialog.set_value('assessment_group_name', assessment_group_name),
			() => cur_dialog.set_value('parent_assessment_group', parent_assessment_group),
			() => vmraid.click_button('Create New'),
		]);
	}
};