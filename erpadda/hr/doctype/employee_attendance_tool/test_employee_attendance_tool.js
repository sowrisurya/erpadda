QUnit.module('hr');

QUnit.test("Test: Employee attendance tool [HR]", function (assert) {
	assert.expect(2);
	let done = assert.async();
	let today_date = vmraid.datetime.nowdate();
	let date_of_attendance = vmraid.datetime.add_days(today_date, -2);	// previous day

	vmraid.run_serially([
		// create employee
		() => {
			return vmraid.tests.make('Employee', [
				{salutation: "Mr"},
				{employee_name: "Test Employee 2"},
				{company: "For Testing"},
				{date_of_joining: vmraid.datetime.add_months(today_date, -2)},	// joined 2 month from now
				{date_of_birth: vmraid.datetime.add_months(today_date, -240)},	// age is 20 years
				{employment_type: "Test Employment type"},
				{holiday_list: "Test Holiday list"},
				{branch: "Test Branch"},
				{department: "Test Department"},
				{designation: "Test Designation"}
			]);
		},
		() => vmraid.set_route("Form", "Employee Attendance Tool"),
		() => vmraid.timeout(0.5),
		() => assert.equal("Employee Attendance Tool", cur_frm.doctype,
			"Form for Employee Attendance Tool opened successfully."),
		// set values in form
		() => cur_frm.set_value("date", date_of_attendance),
		() => cur_frm.set_value("branch", "Test Branch"),
		() => cur_frm.set_value("department", "Test Department"),
		() => cur_frm.set_value("company", "For Testing"),
		() => vmraid.timeout(1),
		() => vmraid.click_button('Check all'),
		() => vmraid.click_button('Mark Present'),
		// check if attendance is marked
		() => vmraid.set_route("List", "Attendance", "List"),
		() => vmraid.timeout(1),
		() => {
			return vmraid.call({
				method: "vmraid.client.get_list",
				args: {
					doctype: "Employee",
					filters: {
						"branch": "Test Branch",
						"department": "Test Department",
						"company": "For Testing",
						"status": "Active"
					}
				},
				callback: function(r) {
					let marked_attendance = cur_list.data.filter(d => d.attendance_date == date_of_attendance);
					assert.equal(marked_attendance.length, r.message.length,
						'all the attendance are marked for correct date');
				}
			});
		},
		() => done()
	]);
});