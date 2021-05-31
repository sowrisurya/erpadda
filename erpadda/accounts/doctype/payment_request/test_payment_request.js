/* eslint-disable */
// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Payment Request", function (assert) {
	let done = assert.async();

	// number of asserts
	assert.expect(1);

	vmraid.run_serially([
		// insert a new Payment Request
		() => vmraid.tests.make('Payment Request', [
			// values to be set
			{key: 'value'}
		]),
		() => {
			assert.equal(cur_frm.doc.key, 'value');
		},
		() => done()
	]);

});
