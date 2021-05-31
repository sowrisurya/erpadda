// Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

vmraid.ui.form.on("Workstation", {
	onload: function(frm) {
		if(frm.is_new())
		{
			vmraid.call({
				type:"GET",
				method:"erpadda.manufacturing.doctype.workstation.workstation.get_default_holiday_list",
				callback: function(r) {
					if(!r.exe && r.message){
						cur_frm.set_value("holiday_list", r.message);
					}
				}
			})
		}
	}
})