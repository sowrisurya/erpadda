QUnit.module('hr');

QUnit.test("Test: Job Offer [HR]", function (assert) {
	assert.expect(3);
	let done = assert.async();
	vmraid.run_serially([
		// Job Offer Creation
		() => {
			vmraid.tests.make('Job Offer', [
				{ job_applicant: 'Utkarsh Goswami - goswamiutkarsh0@gmail.com - software-developer'},
				{ applicant_name: 'Utkarsh Goswami'},
				{ status: 'Accepted'},
				{ designation: 'Software Developer'},
				{ offer_terms: [
					[
						{offer_term: 'Responsibilities'},
						{value: 'Design, installation, testing and maintenance of software systems.'}
					],
					[
						{offer_term: 'Department'},
						{value: 'Research & Development'}
					],
					[
						{offer_term: 'Probationary Period'},
						{value: 'The Probation period is for 3 months.'}
					]
				]},
			]);
		},
		() => vmraid.timeout(10),
		() => vmraid.click_button('Submit'),
		() => vmraid.timeout(2),
		() => vmraid.click_button('Yes'),
		() => vmraid.timeout(5),
		// To check if the fields are correctly set
		() => {
			assert.ok(cur_frm.get_field('status').value=='Accepted',
				'Status of job offer is correct');
			assert.ok(cur_frm.get_field('designation').value=='Software Developer',
				'Designation of applicant is correct');
		},
		() => vmraid.set_route('List','Job Offer','List'),
		() => vmraid.timeout(2),
		// Checking the submission of and Job Offer
		() => {
			assert.ok(cur_list.data[0].docstatus==1,'Job Offer Submitted successfully');
		},
		() => vmraid.timeout(2),
		() => done()
	]);
});