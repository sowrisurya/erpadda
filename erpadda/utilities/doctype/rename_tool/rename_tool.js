// Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


vmraid.ui.form.on("Rename Tool", {
	onload: function(frm) {
		return vmraid.call({
			method: "erpadda.utilities.doctype.rename_tool.rename_tool.get_doctypes",
			callback: function(r) {
				frm.set_df_property("select_doctype", "options", r.message);
			}
		});
	},
	refresh: function(frm) {
		frm.disable_save();
		if (!frm.doc.file_to_rename) {
			frm.get_field("rename_log").$wrapper.html("");
		}
		frm.page.set_primary_action(__("Rename"), function() {
			frm.get_field("rename_log").$wrapper.html("<p>Renaming...</p>");
			vmraid.call({
				method: "erpadda.utilities.doctype.rename_tool.rename_tool.upload",
				args: {
					select_doctype: frm.doc.select_doctype
				},
				callback: function(r) {
					frm.get_field("rename_log").$wrapper.html(r.message.join("<br>"));
				}
			});
		});
	}
})
