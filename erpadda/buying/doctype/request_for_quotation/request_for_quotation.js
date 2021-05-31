// Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


{% include 'erpadda/public/js/controllers/buying.js' %};

cur_frm.add_fetch('contact', 'email_id', 'email_id')

vmraid.ui.form.on("Request for Quotation",{
	setup: function(frm) {
		frm.custom_make_buttons = {
			'Supplier Quotation': 'Create'
		}

		frm.fields_dict["suppliers"].grid.get_field("contact").get_query = function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				query: "erpadda.buying.doctype.request_for_quotation.request_for_quotation.get_supplier_contacts",
				filters: {'supplier': d.supplier}
			}
		}
	},

	onload: function(frm) {
		if(!frm.doc.message_for_supplier) {
			frm.set_value("message_for_supplier", __("Please supply the specified items at the best possible rates"))
		}
	},

	refresh: function(frm, cdt, cdn) {
		if (frm.doc.docstatus === 1) {

			frm.add_custom_button(__('Supplier Quotation'),
				function(){ frm.trigger("make_suppplier_quotation") }, __("Create"));


			frm.add_custom_button(__("Send Emails to Suppliers"), function() {
				vmraid.call({
					method: 'erpadda.buying.doctype.request_for_quotation.request_for_quotation.send_supplier_emails',
					freeze: true,
					args: {
						rfq_name: frm.doc.name
					},
					callback: function(r){
						frm.reload_doc();
					}
				});
			}, __("Tools"));

			frm.add_custom_button(__('Download PDF'), () => {
				var suppliers = [];
				const fields = [{
					fieldtype: 'Link',
					label: __('Select a Supplier'),
					fieldname: 'supplier',
					options: 'Supplier',
					reqd: 1,
					get_query: () => {
						return {
							filters: [
								["Supplier", "name", "in", frm.doc.suppliers.map((row) => {return row.supplier;})]
							]
						}
					}
				}];

				vmraid.prompt(fields, data => {
					var child = locals[cdt][cdn]

					var w = window.open(
						vmraid.urllib.get_full_url("/api/method/erpadda.buying.doctype.request_for_quotation.request_for_quotation.get_pdf?"
						+"doctype="+encodeURIComponent(frm.doc.doctype)
						+"&name="+encodeURIComponent(frm.doc.name)
						+"&supplier="+encodeURIComponent(data.supplier)
						+"&no_letterhead=0"));
					if(!w) {
						vmraid.msgprint(__("Please enable pop-ups")); return;
					}
				},
				'Download PDF for Supplier',
				'Download');
			},
			__("Tools"));

			frm.page.set_inner_btn_group_as_primary(__('Create'));
		}

	},

	make_suppplier_quotation: function(frm) {
		var doc = frm.doc;
		var dialog = new vmraid.ui.Dialog({
			title: __("Create Supplier Quotation"),
			fields: [
				{	"fieldtype": "Select", "label": __("Supplier"),
					"fieldname": "supplier",
					"options": doc.suppliers.map(d => d.supplier),
					"reqd": 1,
					"default": doc.suppliers.length === 1 ? doc.suppliers[0].supplier_name : "" },
			],
			primary_action_label: __("Create"),
			primary_action: (args) => {
				if(!args) return;
				dialog.hide();

				return vmraid.call({
					type: "GET",
					method: "erpadda.buying.doctype.request_for_quotation.request_for_quotation.make_supplier_quotation_from_rfq",
					args: {
						"source_name": doc.name,
						"for_supplier": args.supplier
					},
					freeze: true,
					callback: function(r) {
						if(!r.exc) {
							var doc = vmraid.model.sync(r.message);
							vmraid.set_route("Form", r.message.doctype, r.message.name);
						}
					}
				});
			}
		});

		dialog.show()
	},

	preview: (frm) => {
		let dialog = new vmraid.ui.Dialog({
			title: __('Preview Email'),
			fields: [
				{
					label: __('Supplier'),
					fieldtype: 'Select',
					fieldname: 'supplier',
					options: frm.doc.suppliers.map(row => row.supplier),
					reqd: 1
				},
				{
					fieldtype: 'Column Break',
					fieldname: 'col_break_1',
				},
				{
					label: __('Subject'),
					fieldtype: 'Data',
					fieldname: 'subject',
					read_only: 1,
					depends_on: 'subject'
				},
				{
					fieldtype: 'Section Break',
					fieldname: 'sec_break_1',
					hide_border: 1
				},
				{
					label: __('Email'),
					fieldtype: 'HTML',
					fieldname: 'email_preview'
				},
				{
					fieldtype: 'Section Break',
					fieldname: 'sec_break_2'
				},
				{
					label: __('Note'),
					fieldtype: 'HTML',
					fieldname: 'note'
				}
			]
		});

		dialog.fields_dict['supplier'].df.onchange = () => {
			var supplier = dialog.get_value('supplier');
			frm.call('get_supplier_email_preview', {supplier: supplier}).then(result => {
				dialog.fields_dict.email_preview.$wrapper.empty();
				dialog.fields_dict.email_preview.$wrapper.append(result.message);
			});

		}

		dialog.fields_dict.note.$wrapper.append(`<p class="small text-muted">This is a preview of the email to be sent. A PDF of the document will
			automatically be attached with the email.</p>`);

		dialog.set_value("subject", frm.doc.subject);
		dialog.show();
	}
})

vmraid.ui.form.on("Request for Quotation Supplier",{
	supplier: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn]
		vmraid.call({
			method:"erpadda.accounts.party.get_party_details",
			args:{
				party: d.supplier,
				party_type: 'Supplier'
			},
			callback: function(r){
				if(r.message){
					vmraid.model.set_value(cdt, cdn, 'contact', r.message.contact_person)
					vmraid.model.set_value(cdt, cdn, 'email_id', r.message.contact_email)
				}
			}
		})
	},

})

erpadda.buying.RequestforQuotationController = class RequestforQuotationController extends erpadda.buying.BuyingController {
	refresh() {
		var me = this;
		super.refresh();
		if (this.frm.doc.docstatus===0) {
			this.frm.add_custom_button(__('Material Request'),
				function() {
					erpadda.utils.map_current_doc({
						method: "erpadda.stock.doctype.material_request.material_request.make_request_for_quotation",
						source_doctype: "Material Request",
						target: me.frm,
						setters: {
							schedule_date: undefined,
							status: undefined
						},
						get_query_filters: {
							material_request_type: "Purchase",
							docstatus: 1,
							status: ["!=", "Stopped"],
							per_ordered: ["<", 100],
							company: me.frm.doc.company
						}
					})
				}, __("Get Items From"));

			// Get items from Opportunity
			this.frm.add_custom_button(__('Opportunity'),
				function() {
					erpadda.utils.map_current_doc({
						method: "erpadda.crm.doctype.opportunity.opportunity.make_request_for_quotation",
						source_doctype: "Opportunity",
						target: me.frm,
						setters: {
							party_name: undefined,
							opportunity_from: undefined,
							status: undefined
						},
						get_query_filters: {
							status: ["not in", ["Closed", "Lost"]],
							company: me.frm.doc.company
						}
					})
				}, __("Get Items From"));

			// Get items from open Material Requests based on supplier
			this.frm.add_custom_button(__('Possible Supplier'), function() {
				// Create a dialog window for the user to pick their supplier
				var dialog = new vmraid.ui.Dialog({
					title: __('Select Possible Supplier'),
					fields: [
						{
							fieldname: 'supplier',
							fieldtype:'Link',
							options:'Supplier',
							label:'Supplier',
							reqd:1,
							description: __("Get Items from Material Requests against this Supplier")
						}
					],
					primary_action_label: __("Get Items"),
					primary_action: (args) => {
						if(!args) return;
						dialog.hide();

						erpadda.utils.map_current_doc({
							method: "erpadda.buying.doctype.request_for_quotation.request_for_quotation.get_item_from_material_requests_based_on_supplier",
							source_name: args.supplier,
							target: me.frm,
							setters: {
								company: me.frm.doc.company
							},
							get_query_filters: {
								material_request_type: "Purchase",
								docstatus: 1,
								status: ["!=", "Stopped"],
								per_ordered: ["<", 100]
							}
						});
						dialog.hide();
					}
				});

				dialog.show();
			}, __("Get Items From"));

			// Link Material Requests
			this.frm.add_custom_button(__('Link to Material Requests'),
				function() {
					erpadda.buying.link_to_mrs(me.frm);
				}, __("Tools"));

			// Get Suppliers
			this.frm.add_custom_button(__('Get Suppliers'),
				function() {
					me.get_suppliers_button(me.frm);
				}, __("Tools"));
		}
	}

	calculate_taxes_and_totals() {
		return;
	}

	tc_name() {
		this.get_terms();
	}

	get_suppliers_button (frm) {
		var doc = frm.doc;
		var dialog = new vmraid.ui.Dialog({
			title: __("Get Suppliers"),
			fields: [
				{
					"fieldtype": "Select", "label": __("Get Suppliers By"),
					"fieldname": "search_type",
					"options": ["Supplier Group", "Tag"],
					"reqd": 1,
					onchange() {
						if(dialog.get_value('search_type') == 'Tag'){
							vmraid.call({
								method: 'erpadda.buying.doctype.request_for_quotation.request_for_quotation.get_supplier_tag',
							}).then(r => {
								dialog.set_df_property("tag", "options", r.message)
						});
						}
					}
				},
				{
					"fieldtype": "Link", "label": __("Supplier Group"),
					"fieldname": "supplier_group",
					"options": "Supplier Group",
					"reqd": 0,
					"depends_on": "eval:doc.search_type == 'Supplier Group'"
				},
				{
					"fieldtype": "Select", "label": __("Tag"),
					"fieldname": "tag",
					"reqd": 0,
					"depends_on": "eval:doc.search_type == 'Tag'",
				}
			],
			primary_action_label: __("Add Suppliers"),
			primary_action : (args) => {
				if(!args) return;
				dialog.hide();

				//Remove blanks
				for (var j = 0; j < frm.doc.suppliers.length; j++) {
					if(!frm.doc.suppliers[j].hasOwnProperty("supplier")) {
						frm.get_field("suppliers").grid.grid_rows[j].remove();
					}
				}

				function load_suppliers(r) {
					if(r.message) {
						for (var i = 0; i < r.message.length; i++) {
							var exists = false;
							if (r.message[i].constructor === Array){
								var supplier = r.message[i][0];
							} else {
								var supplier = r.message[i].name;
							}

							for (var j = 0; j < doc.suppliers.length;j++) {
								if (supplier === doc.suppliers[j].supplier) {
									exists = true;
								}
							}
							if(!exists) {
								var d = frm.add_child('suppliers');
								d.supplier = supplier;
								frm.script_manager.trigger("supplier", d.doctype, d.name);
							}
						}
					}
					frm.refresh_field("suppliers");
				}

				if (args.search_type === "Tag" && args.tag) {
					return vmraid.call({
						type: "GET",
						method: "vmraid.desk.doctype.tag.tag.get_tagged_docs",
						args: {
							"doctype": "Supplier",
							"tag": args.tag
						},
						callback: load_suppliers
					});
				} else if (args.supplier_group) {
					return vmraid.call({
						method: "vmraid.client.get_list",
						args: {
							doctype: "Supplier",
							order_by: "name",
							fields: ["name"],
							filters: [["Supplier", "supplier_group", "=", args.supplier_group]]

						},
						callback: load_suppliers
					});
				}
			}
		});

		dialog.show();
	}
};

// for backward compatibility: combine new and previous states
extend_cscript(cur_frm.cscript, new erpadda.buying.RequestforQuotationController({frm: cur_frm}));
