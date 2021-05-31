// Testing Setup Module in education
QUnit.module('education');

QUnit.test('Test: Instructor', function(assert){
	assert.expect(2);
	let done = assert.async();
	vmraid.run_serially([
		() => {
			return vmraid.tests.make("Instructor", [
				{instructor_name: 'Instructor 1'},
				{department: 'Test Department'}
			]);
		},
		() => {
			assert.ok(cur_frm.doc.instructor_name == 'Instructor 1');
			assert.ok(cur_frm.doc.department = 'Test Department');
		},
		() => done()
	]);
});
