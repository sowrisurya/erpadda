/* eslint-disable */
// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Volunteer Type", function (assert) {
	let done = assert.async();

	// number of asserts
	assert.expect(2);

	vmraid.run_serially([
		// insert a new Member
		() => {
			return vmraid.tests.make('Volunteer Type', [
				// values to be set
				{__newname: 'Test Work'},
				{amount: 500}
			]);
		},
		() => {
			assert.equal(cur_frm.doc.name, 'Test Work');
			assert.equal(cur_frm.doc.amount, 500);
		},
		() => done()
	]);

});
