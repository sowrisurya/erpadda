QUnit.module('accounts');

QUnit.test("test account with number", function(assert) {
	assert.expect(7);
	let done = assert.async();
	vmraid.run_serially([
		() => vmraid.set_route('Tree', 'Account'),
		() => vmraid.click_link('Income'),
		() => vmraid.click_button('Add Child'),
		() => vmraid.timeout(.5),
		() => {
			cur_dialog.fields_dict.account_name.$input.val("Test Income");
			cur_dialog.fields_dict.account_number.$input.val("4010");
		},
		() => vmraid.click_button('Create New'),
		() => vmraid.timeout(1),
		() => {
			assert.ok($('a:contains("4010 - Test Income"):visible').length!=0, "Account created with number");
		},
		() => vmraid.click_link('4010 - Test Income'),
		() => vmraid.click_button('Edit'),
		() => vmraid.timeout(.5),
		() => vmraid.click_button('Update Account Number'),
		() => vmraid.timeout(.5),
		() => {
			cur_dialog.fields_dict.account_number.$input.val("4020");
		},
		() => vmraid.timeout(1),
		() => cur_dialog.primary_action(),
		() => vmraid.timeout(1),
		() => cur_frm.refresh_fields(),
		() => vmraid.timeout(.5),
		() => {
			var abbr = vmraid.get_abbr(vmraid.defaults.get_default("Company"));
			var new_account = "4020 - Test Income - " + abbr;
			assert.ok(cur_frm.doc.name==new_account, "Account renamed");
			assert.ok(cur_frm.doc.account_name=="Test Income", "account name remained same");
			assert.ok(cur_frm.doc.account_number=="4020", "Account number updated to 4020");
		},
		() => vmraid.timeout(1),
		() => vmraid.click_button('Menu'),
		() => vmraid.click_link('Rename'),
		() => vmraid.timeout(.5),
		() => {
			cur_dialog.fields_dict.new_name.$input.val("4030 - Test Income");
		},
		() => vmraid.timeout(.5),
		() => vmraid.click_button("Rename"),
		() => vmraid.timeout(2),
		() => {
			assert.ok(cur_frm.doc.account_name=="Test Income", "account name remained same");
			assert.ok(cur_frm.doc.account_number=="4030", "Account number updated to 4030");
		},
		() => vmraid.timeout(.5),
		() => vmraid.click_button('Chart of Accounts'),
		() => vmraid.timeout(.5),
		() => vmraid.click_button('Menu'),
		() => vmraid.click_link('Refresh'),
		() => vmraid.click_button('Expand All'),
		() => vmraid.click_link('4030 - Test Income'),
		() => vmraid.click_button('Delete'),
		() => vmraid.click_button('Yes'),
		() => vmraid.timeout(.5),
		() => {
			assert.ok($('a:contains("4030 - Test Account"):visible').length==0, "Account deleted");
		},
		() => done()
	]);
});
