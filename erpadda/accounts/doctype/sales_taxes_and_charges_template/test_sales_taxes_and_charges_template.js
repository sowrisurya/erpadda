QUnit.module('Sales Taxes and Charges Template');

QUnit.test("test sales taxes and charges template", function(assert) {
	assert.expect(2);
	let done = assert.async();
	vmraid.run_serially([
		() => {
			return vmraid.tests.make('Sales Taxes and Charges Template', [
				{title: "TEST In State GST"},
				{taxes:[
					[
						{charge_type:"On Net Total"},
						{account_head:"CGST - "+vmraid.get_abbr(vmraid.defaults.get_default("Company")) }
					],
					[
						{charge_type:"On Net Total"},
						{account_head:"SGST - "+vmraid.get_abbr(vmraid.defaults.get_default("Company")) }
					]
				]}
			]);
		},
		() => {
			assert.ok(cur_frm.doc.title=='TEST In State GST');
			assert.ok(cur_frm.doc.name=='TEST In State GST - FT');
		},
		() => done()
	]);
});

