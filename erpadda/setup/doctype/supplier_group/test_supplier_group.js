/* eslint-disable */
// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Supplier Group", function (assert) {
	let done = assert.async();

	// number of asserts
	assert.expect(1);

	vmraid.run_serially([
		// insert a new Supplier Group
		() => vmraid.tests.make('Supplier Group', [
			// values to be set
			{key: 'value'}
		]),
		() => {
			assert.equal(cur_frm.doc.key, 'value');
		},
		() => done()
	]);

});
