QUnit.module('HR');

QUnit.test("test: Payroll Entry", function (assert) {
	assert.expect(5);
	let done = assert.async();
	let employees, docname;

	vmraid.run_serially([
		() => {
			return vmraid.tests.make('Payroll Entry', [
				{company: 'For Testing'},
				{posting_date: vmraid.datetime.add_days(vmraid.datetime.nowdate(), 0)},
				{payroll_frequency: 'Monthly'},
				{cost_center: 'Main - '+vmraid.get_abbr(vmraid.defaults.get_default("Company"))}
			]);
		},

		() => vmraid.timeout(1),
		() => {
			assert.equal(cur_frm.doc.company, 'For Testing');
			assert.equal(cur_frm.doc.posting_date, vmraid.datetime.add_days(vmraid.datetime.nowdate(), 0));
			assert.equal(cur_frm.doc.cost_center, 'Main - FT');
		},
		() => vmraid.click_button('Get Employee Details'),
		() => {
			employees = cur_frm.doc.employees.length;
			docname = cur_frm.doc.name;
		},

		() => vmraid.click_button('Submit'),
		() => vmraid.timeout(1),
		() => vmraid.click_button('Yes'),
		() => vmraid.timeout(5),

		() => vmraid.click_button('View Salary Slip'),
		() => vmraid.timeout(2),
		() => assert.equal(cur_list.data.length, employees),

		() => vmraid.set_route('Form', 'Payroll Entry', docname),
		() => vmraid.timeout(2),
		() => vmraid.click_button('Submit Salary Slip'),
		() => vmraid.click_button('Yes'),
		() => vmraid.timeout(5),

		() => vmraid.click_button('Close'),
		() => vmraid.timeout(1),

		() => vmraid.click_button('View Salary Slip'),
		() => vmraid.timeout(2),
		() => {
			let count = 0;
			for(var i = 0; i < employees; i++) {
				if(cur_list.data[i].docstatus == 1){
					count++;
				}
			}
			assert.equal(count, employees, "Salary Slip submitted for all employees");
		},

		() => done()
	]);
});
