QUnit.module('setup');

QUnit.test("Test: Company [SetUp]", function (assert) {
	assert.expect(2);
	let done = assert.async();

	vmraid.run_serially([
		// test company creation
		() => vmraid.set_route("List", "Company", "List"),
		() => vmraid.new_doc("Company"),
		() => vmraid.timeout(1),
		() => cur_frm.set_value("company_name", "Test Company"),
		() => cur_frm.set_value("abbr", "TC"),
		() => cur_frm.set_value("domain", "Services"),
		() => cur_frm.set_value("default_currency", "INR"),
		// save form
		() => cur_frm.save(),
		() => vmraid.timeout(1),
		() => assert.equal("Debtors - TC", cur_frm.doc.default_receivable_account,
			'chart of acounts created'),
		() => assert.equal("Main - TC", cur_frm.doc.cost_center,
			'chart of cost centers created'),
		() => done()
	]);
});