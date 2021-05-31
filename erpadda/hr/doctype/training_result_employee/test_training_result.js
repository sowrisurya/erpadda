QUnit.module('hr');

QUnit.test("Test: Training Result [HR]", function (assert) {
	assert.expect(5);
	let done = assert.async();
	vmraid.run_serially([
		// Creating Training Result
		() => vmraid.set_route('List','Training Result','List'),
		() => vmraid.timeout(0.3),
		() => vmraid.click_button('Make a new Training Result'),
		() => {
			cur_frm.set_value('training_event','Test Training Event 1');
		},
		() => vmraid.timeout(1),
		() => vmraid.model.set_value('Training Result Employee','New Training Result Employee 1','hours',4),
		() => vmraid.model.set_value('Training Result Employee','New Training Result Employee 1','grade','A'),
		() => vmraid.model.set_value('Training Result Employee','New Training Result Employee 1','comments','Nice Seminar'),
		() => vmraid.timeout(1),
		() => cur_frm.save(),
		() => vmraid.timeout(1),
		() => cur_frm.save(),

		// Submitting the Training Result
		() => vmraid.click_button('Submit'),
		() => vmraid.click_button('Yes'),
		() => vmraid.timeout(4),

		// Checking if the fields are correctly set
		() => {
			assert.equal('Test Training Event 1',cur_frm.get_field('training_event').value,
				'Training Result is created');

			assert.equal('Test Employee 1',cur_frm.doc.employees[0].employee_name,
				'Training Result is created for correct employee');

			assert.equal(4,cur_frm.doc.employees[0].hours,
				'Hours field is correctly calculated');

			assert.equal('A',cur_frm.doc.employees[0].grade,
				'Grade field is correctly set');
		},

		() => vmraid.set_route('List','Training Result','List'),
		() => vmraid.timeout(2),

		// Checking the submission of Training Result
		() => {
			assert.ok(cur_list.data[0].docstatus==1,'Training Result Submitted successfully');
		},
		() => done()
	]);
});

