/* eslint-disable */
// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Donor Type", function (assert) {
	let done = assert.async();

	// number of asserts
	assert.expect(1);

	vmraid.run_serially([
		// insert a new Member
		() => vmraid.tests.make('Donor Type', [
			// values to be set
			{donor_type: 'Test Organization'},
		]),
		() => {
			assert.equal(cur_frm.doc.donor_type, 'Test Organization');
		},
		() => done()
	]);

});
