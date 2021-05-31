// Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('Hotel Room Reservation', {
	refresh: function(frm) {
		if(frm.doc.docstatus == 1){
			frm.add_custom_button(__('Create Invoice'), ()=> {
				frm.trigger("make_invoice");
			});
		}
	},
	from_date: function(frm) {
		frm.trigger("recalculate_rates");
	},
	to_date: function(frm) {
		frm.trigger("recalculate_rates");
	},
	recalculate_rates: function(frm) {
		if (!frm.doc.from_date || !frm.doc.to_date
			|| !frm.doc.items.length){
			return;
		}
		vmraid.call({
			"method": "erpadda.hotels.doctype.hotel_room_reservation.hotel_room_reservation.get_room_rate",
			"args": {"hotel_room_reservation": frm.doc}
		}).done((r)=> {
			for (var i = 0; i < r.message.items.length; i++) {
				frm.doc.items[i].rate = r.message.items[i].rate;
				frm.doc.items[i].amount = r.message.items[i].amount;
			}
			vmraid.run_serially([
				()=> frm.set_value("net_total", r.message.net_total),
				()=> frm.refresh_field("items")
			]);
		});
	},
	make_invoice: function(frm) {
		vmraid.model.with_doc("Hotel Settings", "Hotel Settings", ()=>{
			vmraid.model.with_doctype("Sales Invoice", ()=>{
				let hotel_settings = vmraid.get_doc("Hotel Settings", "Hotel Settings");
				let invoice = vmraid.model.get_new_doc("Sales Invoice");
				invoice.customer = frm.doc.customer || hotel_settings.default_customer;
				if (hotel_settings.default_invoice_naming_series){
					invoice.naming_series = hotel_settings.default_invoice_naming_series;
				}
				for (let d of frm.doc.items){
					let invoice_item = vmraid.model.add_child(invoice, "items")
					invoice_item.item_code = d.item;
					invoice_item.qty = d.qty;
					invoice_item.rate = d.rate;
				}
				if (hotel_settings.default_taxes_and_charges){
					invoice.taxes_and_charges = hotel_settings.default_taxes_and_charges;
				}
				vmraid.set_route("Form", invoice.doctype, invoice.name);
			});
		});
	}
});

vmraid.ui.form.on('Hotel Room Reservation Item', {
	item: function(frm, doctype, name) {
		frm.trigger("recalculate_rates");
	},
	qty: function(frm) {
		frm.trigger("recalculate_rates");
	}
});
