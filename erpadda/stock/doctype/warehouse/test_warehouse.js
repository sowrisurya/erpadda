QUnit.test("test: warehouse", function (assert) {
	assert.expect(0);
	let done = assert.async();

	vmraid.run_serially([
		// test warehouse creation
		() => vmraid.set_route("List", "Warehouse"),

		// Create a Laptop Scrap Warehouse
		() => vmraid.tests.make(
			"Warehouse", [
				{warehouse_name: "Laptop Scrap Warehouse"},
				{company: "For Testing"}
			]
		),

		() => done()
	]);
});