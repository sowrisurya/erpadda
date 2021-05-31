// Education Assessment module
QUnit.module('education');

QUnit.test('Test: Assessment Criteria', function(assert){
	assert.expect(0);
	let done = assert.async();
	vmraid.run_serially([
		() => {
			return vmraid.tests.make('Assessment Criteria', [
				{assessment_criteria: 'Pass'},
				{assessment_criteria_group: 'Reservation'}
			]);
		},
		() => done()
	]);
});