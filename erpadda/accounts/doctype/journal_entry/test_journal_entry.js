QUnit.module('Journal Entry');

QUnit.test("test journal entry", function(assert) {
	assert.expect(2);
	let done = assert.async();
	vmraid.run_serially([
		() => {
			return vmraid.tests.make('Journal Entry', [
				{posting_date:vmraid.datetime.add_days(vmraid.datetime.nowdate(), 0)},
				{accounts: [
					[
						{'account':'Debtors - '+vmraid.get_abbr(vmraid.defaults.get_default('Company'))},
						{'party_type':'Customer'},
						{'party':'Test Customer 1'},
						{'credit_in_account_currency':1000},
						{'is_advance':'Yes'},
					],
					[
						{'account':'HDFC - '+vmraid.get_abbr(vmraid.defaults.get_default('Company'))},
						{'debit_in_account_currency':1000},
					]
				]},
				{cheque_no:1234},
				{cheque_date: vmraid.datetime.add_days(vmraid.datetime.nowdate(), -1)},
				{user_remark: 'Test'},
			]);
		},
		() => cur_frm.save(),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.total_debit==1000, "total debit correct");
			assert.ok(cur_frm.doc.total_credit==1000, "total credit correct");
		},
		() => vmraid.tests.click_button('Submit'),
		() => vmraid.tests.click_button('Yes'),
		() => vmraid.timeout(0.3),
		() => done()
	]);
});
