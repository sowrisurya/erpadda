QUnit.test("test: operation", function (assert) {
	assert.expect(2);
	let done = assert.async();
	vmraid.run_serially([
		// test operation creation
		() => vmraid.set_route("List", "Operation"),

		// Create a Keyboard operation
		() => {
			return vmraid.tests.make(
				"Operation", [
					{__newname: "Assemble Keyboard"},
					{workstation: "Keyboard assembly workstation"}
				]
			);
		},
		() => vmraid.timeout(3),
		() => {
			assert.ok(cur_frm.docname.includes('Assemble Keyboard'),
				'Assemble Keyboard created successfully');
			assert.ok(cur_frm.doc.workstation.includes('Keyboard assembly workstation'),
				'Keyboard assembly workstation was linked successfully');
		},

		// Create a Screen operation
		() => {
			return vmraid.tests.make(
				"Operation", [
					{__newname: 'Assemble Screen'},
					{workstation: "Screen assembly workstation"}
				]
			);
		},
		() => vmraid.timeout(3),

		// Create a CPU operation
		() => {
			return vmraid.tests.make(
				"Operation", [
					{__newname: 'Assemble CPU'},
					{workstation: "CPU assembly workstation"}
				]
			);
		},
		() => vmraid.timeout(3),

		() => done()
	]);
});
