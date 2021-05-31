QUnit.module("sales");

QUnit.test("test: lead", function (assert) {
	assert.expect(4);
	let done = assert.async();
	let lead_name = vmraid.utils.get_random(10);
	vmraid.run_serially([
		// test lead creation
		() => vmraid.set_route("List", "Lead"),
		() => vmraid.new_doc("Lead"),
		() => vmraid.timeout(1),
		() => cur_frm.set_value("lead_name", lead_name),
		() => cur_frm.save(),
		() => vmraid.timeout(1),
		() => {
			assert.ok(cur_frm.doc.lead_name.includes(lead_name),
				'name correctly set');
			vmraid.lead_name = cur_frm.doc.name;
		},
		// create address and contact
		() => vmraid.click_link('Address & Contact'),
		() => vmraid.click_button('New Address'),
		() => vmraid.timeout(1),
		() => vmraid.set_control('address_line1', 'Gateway'),
		() => vmraid.set_control('city', 'Mumbai'),
		() => cur_frm.save(),
		() => vmraid.timeout(3),
		() => assert.equal(vmraid.get_route()[1], 'Lead',
			'back to lead form'),
		() => vmraid.click_link('Address & Contact'),
		() => assert.ok($('.address-box').text().includes('Mumbai'),
			'city is seen in address box'),

		// make opportunity
		() => vmraid.click_button('Make'),
		() => vmraid.click_link('Opportunity'),
		() => vmraid.timeout(2),
		() => assert.equal(cur_frm.doc.lead, vmraid.lead_name,
			'lead name correctly mapped'),

		() => done()
	]);
});
