// Testing Admission module in Education
QUnit.module('education');

QUnit.test('test student applicant', function(assert){
	assert.expect(11);
	let done = assert.async();
	let testing_status;
	vmraid.run_serially([
		() => vmraid.set_route('List', 'Student Applicant'),
		() => vmraid.timeout(0.5),
		() => {$(`a:contains("Fname Mname Lname"):visible`)[0].click();},

		// Checking different options
		// 1. Moving forward with Submit
		() => vmraid.timeout(0.5),
		() => vmraid.tests.click_button('Submit'),
		() => vmraid.tests.click_button('Yes'),
		() => vmraid.timeout(0.5),
		() => {
			testing_status = $('span.indicator.orange').text();
			assert.ok(testing_status.indexOf('Submit this document to confirm') == -1); // checking if submit has been successfull
		},

		// 2. Cancelling the Submit request
		() => vmraid.timeout(0.5),
		() => vmraid.tests.click_button('Cancel'),
		() => vmraid.tests.click_button('Yes'),
		() => vmraid.timeout(0.5),
		() => {
			testing_status = $('h1.editable-title').text();
			assert.ok(testing_status.indexOf('Cancelled') != -1); // checking if cancel request has been successfull
		},

		// 3. Checking Amend option
		() => vmraid.timeout(0.5),
		() => vmraid.tests.click_button('Amend'),
		() => cur_frm.doc.student_email_id = "test2@testmail.com", // updating email id since same id again is not allowed
		() => cur_frm.save(),
		() => vmraid.timeout(0.5),
		() => vmraid.tests.click_button('Submit'),
		() => vmraid.tests.click_button('Yes'), // Submitting again after amend
		() => {
			testing_status = $('span.indicator.orange').text();
			assert.ok(testing_status.indexOf('Submit this document to confirm') == -1); // checking if submit has been successfull after amend
		},

		// Checking different Application status option
		() => {
			testing_status = $('h1.editable-title').text();
			assert.ok(testing_status.indexOf('Applied') != -1); // checking if Applied has been successfull
		},
		() => cur_frm.set_value('application_status', "Rejected"), // Rejected Status
		() => vmraid.tests.click_button('Update'),
		() => {
			testing_status = $('h1.editable-title').text();
			assert.ok(testing_status.indexOf('Rejected') != -1); // checking if Rejected has been successfull
		},
		() => cur_frm.set_value('application_status', "Admitted"), // Admitted Status
		() => vmraid.tests.click_button('Update'),
		() => {
			testing_status = $('h1.editable-title').text();
			assert.ok(testing_status.indexOf('Admitted') != -1); // checking if Admitted has been successfull
		},
		() => cur_frm.set_value('application_status', "Approved"), // Approved Status
		() => vmraid.tests.click_button('Update'),
		() => {
			testing_status = $('h1.editable-title').text();
			assert.ok(testing_status.indexOf('Approved') != -1); // checking if Approved has been successfull
		},

		// Clicking on Enroll button should add the applicant's entry in Student doctype, and take you to Program Enrollment page
		() => vmraid.timeout(0.5),
		() => vmraid.tests.click_button('Enroll'),
		() => vmraid.timeout(0.5),
		() => {
			assert.ok(vmraid.get_route()[0] == 'Form'); // Checking if the current page is Program Enrollment page or not
			assert.ok(vmraid.get_route()[1] == 'Program Enrollment');
		},

		// Routing to Student List to check if the Applicant's entry has been made or not
		() => vmraid.timeout(0.5),
		() => vmraid.set_route('List', 'Student'),
		() => vmraid.timeout(0.5),
		() => {$(`a:contains("Fname Mname Lname"):visible`)[0].click();},
		() => vmraid.timeout(0.5),
		() => {assert.ok(($(`h1.editable-title`).text()).indexOf('Enabled') != -1, 'Student entry successfully created');}, // Checking if the Student entry has been enabled
		// Enrolling the Student into a Program
		() => {$('.form-documents .row:nth-child(1) .col-xs-6:nth-child(1) .octicon-plus').click();},
		() => vmraid.timeout(1),
		() => cur_frm.set_value('program', 'Standard Test'),
		() => vmraid.timeout(1),
		() => {
			cur_frm.set_value('student_category', 'Reservation');
			cur_frm.set_value('student_batch_name', 'A');
			cur_frm.set_value('academic_year', '2016-17');
			cur_frm.set_value('academic_term', '2016-17 (Semester 1)');
			cur_frm.set_value('school_house', 'Test_house');
		},
		() => cur_frm.save(),

		// Submitting Program Enrollment form for our Test Student
		() => vmraid.timeout(1),
		() => vmraid.tests.click_button('Submit'),
		() => vmraid.tests.click_button('Yes'),
		() => {
			assert.ok(cur_frm.doc.docstatus == 1, "Program enrollment successfully submitted");
		},
		() => done()
	]);
});