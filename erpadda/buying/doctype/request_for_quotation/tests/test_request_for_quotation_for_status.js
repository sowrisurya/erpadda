QUnit.module('buying');

QUnit.test("Test: Request for Quotation", function (assert) {
	assert.expect(5);
	let done = assert.async();
	let rfq_name = "";

	vmraid.run_serially([
		// Go to RFQ list
		() => vmraid.set_route("List", "Request for Quotation"),
		// Create a new RFQ
		() => vmraid.new_doc("Request for Quotation"),
		() => vmraid.timeout(1),
		() => cur_frm.set_value("transaction_date", "04-04-2017"),
		() => cur_frm.set_value("company", "For Testing"),
		// Add Suppliers
		() => {
			cur_frm.fields_dict.suppliers.grid.grid_rows[0].toggle_view();
		},
		() => vmraid.timeout(1),
		() => {
			cur_frm.fields_dict.suppliers.grid.grid_rows[0].doc.supplier = "_Test Supplier";
			vmraid.click_check('Send Email');
			cur_frm.cur_grid.frm.script_manager.trigger('supplier');
		},
		() => vmraid.timeout(1),
		() => {
			cur_frm.cur_grid.toggle_view();
		},
		() => vmraid.timeout(1),
		() => vmraid.click_button('Add Row',0),
		() => vmraid.timeout(1),
		() => {
			cur_frm.fields_dict.suppliers.grid.grid_rows[1].toggle_view();
		},
		() => vmraid.timeout(1),
		() => {
			cur_frm.fields_dict.suppliers.grid.grid_rows[1].doc.supplier = "_Test Supplier 1";
			vmraid.click_check('Send Email');
			cur_frm.cur_grid.frm.script_manager.trigger('supplier');
		},
		() => vmraid.timeout(1),
		() => {
			cur_frm.cur_grid.toggle_view();
		},
		() => vmraid.timeout(1),
		// Add Item
		() => {
			cur_frm.fields_dict.items.grid.grid_rows[0].toggle_view();
		},
		() => vmraid.timeout(1),
		() => {
			cur_frm.fields_dict.items.grid.grid_rows[0].doc.item_code = "_Test Item";
			vmraid.set_control('item_code',"_Test Item");
			vmraid.set_control('qty',5);
			vmraid.set_control('schedule_date', "05-05-2017");
			cur_frm.cur_grid.frm.script_manager.trigger('supplier');
		},
		() => vmraid.timeout(2),
		() => {
			cur_frm.cur_grid.toggle_view();
		},
		() => vmraid.timeout(2),
		() => {
			cur_frm.fields_dict.items.grid.grid_rows[0].doc.warehouse = "_Test Warehouse - FT";
		},
		() => vmraid.click_button('Save'),
		() => vmraid.timeout(1),
		() => vmraid.click_button('Submit'),
		() => vmraid.timeout(1),
		() => vmraid.click_button('Yes'),
		() => vmraid.timeout(1),
		() => vmraid.click_button('Menu'),
		() => vmraid.timeout(1),
		() => vmraid.click_link('Reload'),
		() => vmraid.timeout(1),
		() => {
			assert.equal(cur_frm.doc.docstatus, 1);
			rfq_name = cur_frm.doc.name;
			assert.ok(cur_frm.fields_dict.suppliers.grid.grid_rows[0].doc.quote_status == "Pending");
			assert.ok(cur_frm.fields_dict.suppliers.grid.grid_rows[1].doc.quote_status == "Pending");
		},
		() => {
			cur_frm.fields_dict.suppliers.grid.grid_rows[0].toggle_view();
		},
		() => vmraid.timeout(1),
		() => vmraid.timeout(1),
		() => {
			cur_frm.cur_grid.toggle_view();
		},
		() => vmraid.click_button('Update'),
		() => vmraid.timeout(1),

		() => vmraid.click_button('Supplier Quotation'),
		() => vmraid.timeout(1),
		() => vmraid.click_link('Make'),
		() => vmraid.timeout(1),
		() => {
			vmraid.set_control('supplier',"_Test Supplier 1");
		},
		() => vmraid.timeout(1),
		() => vmraid.click_button('Make Supplier Quotation'),
		() => vmraid.timeout(1),
		() => cur_frm.set_value("company", "For Testing"),
		() => cur_frm.fields_dict.items.grid.grid_rows[0].doc.rate = 4.99,
		() => vmraid.timeout(1),
		() => vmraid.click_button('Save'),
		() => vmraid.timeout(1),
		() => vmraid.click_button('Submit'),
		() => vmraid.timeout(1),
		() => vmraid.click_button('Yes'),
		() => vmraid.timeout(1),
		() => vmraid.set_route("List", "Request for Quotation"),
		() => vmraid.timeout(2),
		() => vmraid.set_route("List", "Request for Quotation"),
		() => vmraid.timeout(2),
		() => vmraid.click_link(rfq_name),
		() => vmraid.timeout(1),
		() => vmraid.click_button('Menu'),
		() => vmraid.timeout(1),
		() => vmraid.click_link('Reload'),
		() => vmraid.timeout(1),
		() => {
			assert.ok(cur_frm.fields_dict.suppliers.grid.grid_rows[1].doc.quote_status == "Received");
		},
		() => done()
	]);
});