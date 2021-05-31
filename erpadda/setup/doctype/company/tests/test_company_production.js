QUnit.test("Test: Company", function (assert) {
	assert.expect(0);

	let done = assert.async();

	vmraid.run_serially([
		// Added company for Work Order testing
		() => vmraid.set_route("List", "Company"),
		() => vmraid.new_doc("Company"),
		() => vmraid.timeout(1),
		() => cur_frm.set_value("company_name", "For Testing"),
		() => cur_frm.set_value("abbr", "RB"),
		() => cur_frm.set_value("default_currency", "INR"),
		() => cur_frm.save(),
		() => vmraid.timeout(1),

		() => done()
	]);
});