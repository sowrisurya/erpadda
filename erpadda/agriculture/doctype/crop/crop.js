// Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.provide("erpadda.crop");

vmraid.ui.form.on('Crop', {
	refresh: (frm) => {
		frm.fields_dict.materials_required.grid.set_column_disp('bom_no', false);
	}
});

vmraid.ui.form.on("BOM Item", {
	item_code: (frm, cdt, cdn) => {
		erpadda.crop.update_item_rate_uom(frm, cdt, cdn);
	},
	qty: (frm, cdt, cdn) => {
		erpadda.crop.update_item_qty_amount(frm, cdt, cdn);
	},
	rate: (frm, cdt, cdn) => {
		erpadda.crop.update_item_qty_amount(frm, cdt, cdn);
	}
});

erpadda.crop.update_item_rate_uom = function(frm, cdt, cdn) {
	let material_list = ['materials_required', 'produce', 'byproducts'];
	material_list.forEach((material) => {
		frm.doc[material].forEach((item, index) => {
			if (item.name == cdn && item.item_code){
				vmraid.call({
					method:'erpadda.agriculture.doctype.crop.crop.get_item_details',
					args: {
						item_code: item.item_code
					},
					callback: (r) => {
						vmraid.model.set_value('BOM Item', item.name, 'uom', r.message.uom);
						vmraid.model.set_value('BOM Item', item.name, 'rate', r.message.rate);
					}
				});
			}
		});
	});
};

erpadda.crop.update_item_qty_amount = function(frm, cdt, cdn) {
	let material_list = ['materials_required', 'produce', 'byproducts'];
	material_list.forEach((material) => {
		frm.doc[material].forEach((item, index) => {
			if (item.name == cdn){
				if (!vmraid.model.get_value('BOM Item', item.name, 'qty'))
					vmraid.model.set_value('BOM Item', item.name, 'qty', 1);
				vmraid.model.set_value('BOM Item', item.name, 'amount', item.qty * item.rate);
			}
		});
	});
};