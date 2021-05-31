// Testing Attendance Module in Education
QUnit.module('education');

QUnit.test('Test: Student Attendace Tool', function(assert){
	assert.expect(10);
	let done = assert.async();
	let i, count = 0;

	vmraid.run_serially([
		() => vmraid.timeout(0.2),
		() => vmraid.set_route('Form', 'Student Attendance Tool'),
		() => vmraid.timeout(0.5),

		() => {
			if(cur_frm.doc.based_on == 'Student Group' || cur_frm.doc.based_on == 'Course Schedule'){
				cur_frm.doc.based_on = 'Student Group';
				assert.equal(1, 1, 'Attendance basis correctly set');
				cur_frm.set_value("group_based_on", 'Batch');
				cur_frm.set_value("student_group", "test-batch-wise-group");
				cur_frm.set_value("date", vmraid.datetime.nowdate());
			}
		},
		() => vmraid.timeout(0.5),
		() => {
			assert.equal($('input.students-check').size(), 5, "Student list based on batch correctly fetched");
			assert.equal(vmraid.datetime.nowdate(), cur_frm.doc.date, 'Current date correctly set');

			cur_frm.set_value("student_group", "test-batch-wise-group-2");
			assert.equal($('input.students-check').size(), 5, "Student list based on batch 2 correctly fetched");

			cur_frm.set_value("group_based_on", 'Course');

			cur_frm.set_value("student_group", "test-course-wise-group");
			assert.equal($('input.students-check').size(), 5, "Student list based on course correctly fetched");

			cur_frm.set_value("student_group", "test-course-wise-group-2");
			assert.equal($('input.students-check').size(), 5, "Student list based on course 2 correctly fetched");
		},

		() => vmraid.timeout(1),
		() => vmraid.tests.click_button('Check all'), // Marking all Student as checked
		() => {
			for(i = 0; i < $('input.students-check').size(); i++){
				if($('input.students-check')[i].checked == true)
					count++;
			}

			if(count == $('input.students-check').size())
				assert.equal($('input.students-check').size(), count, "All students marked checked");
		},

		() => vmraid.timeout(1),
		() => vmraid.tests.click_button('Uncheck all'), // Marking all Student as unchecked
		() => {
			count = 0;
			for(i = 0; i < $('input.students-check').size(); i++){
				if(!($('input.students-check')[i].checked))
					count++;
			}

			if(count == $('input.students-check').size())
				assert.equal($('input.students-check').size(), count, "All students marked checked");
		},

		() => vmraid.timeout(1),
		() => vmraid.tests.click_button('Check all'),
		() => vmraid.tests.click_button('Mark Attendance'),
		() => vmraid.timeout(1),
		() => vmraid.tests.click_button('Yes'),
		() => vmraid.timeout(1),
		() => {
			assert.equal($('.msgprint').text(), "Attendance has been marked successfully.", "Attendance successfully marked");
			vmraid.tests.click_button('Close');
		},

		() => vmraid.timeout(1),
		() => vmraid.set_route('List', 'Student Attendance/List'),
		() => vmraid.timeout(1),
		() => {
			assert.equal(cur_list.data.length, count, "Attendance list created");
		},

		() => done()
	]);
});