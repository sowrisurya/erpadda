QUnit.module("sales");

QUnit.test("test: lead", function (assert) {
	assert.expect(5);
	let done = assert.async();
	let lead_name = vmraid.utils.get_random(10);
	vmraid.run_serially([
		// test lead creation
		() => vmraid.set_route("List", "Lead"),
		() => vmraid.new_doc("Lead"),
		() => vmraid.timeout(1),
		() => cur_frm.set_value("organization_lead", "1"),
		() => cur_frm.set_value("company_name", lead_name),
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

		() => vmraid.click_button('New Contact'),
		() => vmraid.timeout(1),
		() => vmraid.set_control('first_name', 'John'),
		() => vmraid.set_control('last_name', 'Doe'),
		() => cur_frm.save(),
		() => vmraid.timeout(3),
		() => vmraid.set_route('Form', 'Lead', cur_frm.doc.links[0].link_name),
		() => vmraid.timeout(1),
		() => vmraid.click_link('Address & Contact'),
		() => assert.ok($('.address-box').text().includes('John'),
			'contact is seen in contact box'),

		// make customer
		() => vmraid.click_button('Make'),
		() => vmraid.click_link('Customer'),
		() => vmraid.timeout(2),
		() => assert.equal(cur_frm.doc.lead_name, vmraid.lead_name,
			'lead name correctly mapped'),

		() => done()
	]);
});
