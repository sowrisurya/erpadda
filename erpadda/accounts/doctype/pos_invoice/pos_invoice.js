// Copyright (c) 2020, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

{% include 'erpadda/selling/sales_common.js' %};
vmraid.provide("erpadda.accounts");

erpadda.selling.POSInvoiceController = class POSInvoiceController extends erpadda.selling.SellingController {
	setup(doc) {
		this.setup_posting_date_time_check();
		super.setup(doc);
	}

	company() {
		erpadda.accounts.dimensions.update_dimension(this.frm, this.frm.doctype);
	}

	onload(doc) {
		super.onload();
		this.frm.ignore_doctypes_on_cancel_all = ['POS Invoice Merge Log'];
		if(doc.__islocal && doc.is_pos && vmraid.get_route_str() !== 'point-of-sale') {
			this.frm.script_manager.trigger("is_pos");
			this.frm.refresh_fields();
		}

		erpadda.accounts.dimensions.setup_dimension_filters(this.frm, this.frm.doctype);
	}

	refresh(doc) {
		super.refresh();
		if (doc.docstatus == 1 && !doc.is_return) {
			this.frm.add_custom_button(__('Return'), this.make_sales_return, __('Create'));
			this.frm.page.set_inner_btn_group_as_primary(__('Create'));
		}

		if (doc.is_return && doc.__islocal) {
			this.frm.return_print_format = "Sales Invoice Return";
			this.frm.set_value('consolidated_invoice', '');
		}
	}

	is_pos() {
		this.set_pos_data();
	}

	async set_pos_data() {
		if(this.frm.doc.is_pos) {
			this.frm.set_value("allocate_advances_automatically", 0);
			if(!this.frm.doc.company) {
				this.frm.set_value("is_pos", 0);
				vmraid.msgprint(__("Please specify Company to proceed"));
			} else {
				const r = await this.frm.call({
					doc: this.frm.doc,
					method: "set_missing_values",
					freeze: true
				});
				if(!r.exc) {
					if(r.message) {
						this.frm.pos_print_format = r.message.print_format || "";
						this.frm.meta.default_print_format = r.message.print_format || "";
						this.frm.doc.campaign = r.message.campaign;
						this.frm.allow_print_before_pay = r.message.allow_print_before_pay;
					}
					this.frm.script_manager.trigger("update_stock");
					this.calculate_taxes_and_totals();
					this.frm.doc.taxes_and_charges && this.frm.script_manager.trigger("taxes_and_charges");
					vmraid.model.set_default_values(this.frm.doc);
					this.set_dynamic_labels();
				}
			}
		}
	}

	customer() {
		if (!this.frm.doc.customer) return
		const pos_profile = this.frm.doc.pos_profile;
		if(this.frm.updating_party_details) return;
		erpadda.utils.get_party_details(this.frm,
			"erpadda.accounts.party.get_party_details", {
				posting_date: this.frm.doc.posting_date,
				party: this.frm.doc.customer,
				party_type: "Customer",
				account: this.frm.doc.debit_to,
				price_list: this.frm.doc.selling_price_list,
				pos_profile: pos_profile
			}, () => {
				this.apply_pricing_rule();
			});
	}

	amount(){
		this.write_off_outstanding_amount_automatically()
	}

	change_amount(){
		if(this.frm.doc.paid_amount > this.frm.doc.grand_total){
			this.calculate_write_off_amount();
		}else {
			this.frm.set_value("change_amount", 0.0);
			this.frm.set_value("base_change_amount", 0.0);
		}

		this.frm.refresh_fields();
	}

	loyalty_amount(){
		this.calculate_outstanding_amount();
		this.frm.refresh_field("outstanding_amount");
		this.frm.refresh_field("paid_amount");
		this.frm.refresh_field("base_paid_amount");
	}

	write_off_outstanding_amount_automatically() {
		if(cint(this.frm.doc.write_off_outstanding_amount_automatically)) {
			vmraid.model.round_floats_in(this.frm.doc, ["grand_total", "paid_amount"]);
			// this will make outstanding amount 0
			this.frm.set_value("write_off_amount",
				flt(this.frm.doc.grand_total - this.frm.doc.paid_amount - this.frm.doc.total_advance, precision("write_off_amount"))
			);
			this.frm.toggle_enable("write_off_amount", false);

		} else {
			this.frm.toggle_enable("write_off_amount", true);
		}

		this.calculate_outstanding_amount(false);
		this.frm.refresh_fields();
	}

	make_sales_return() {
		vmraid.model.open_mapped_doc({
			method: "erpadda.accounts.doctype.pos_invoice.pos_invoice.make_sales_return",
			frm: cur_frm
		})
	}
}

extend_cscript(cur_frm.cscript, new erpadda.selling.POSInvoiceController({ frm: cur_frm }))

vmraid.ui.form.on('POS Invoice', {
	redeem_loyalty_points: function(frm) {
		frm.events.get_loyalty_details(frm);
	},

	loyalty_points: function(frm) {
		if (frm.redemption_conversion_factor) {
			frm.events.set_loyalty_points(frm);
		} else {
			vmraid.call({
				method: "erpadda.accounts.doctype.loyalty_program.loyalty_program.get_redeemption_factor",
				args: {
					"loyalty_program": frm.doc.loyalty_program
				},
				callback: function(r) {
					if (r) {
						frm.redemption_conversion_factor = r.message;
						frm.events.set_loyalty_points(frm);
					}
				}
			});
		}
	},

	get_loyalty_details: function(frm) {
		if (frm.doc.customer && frm.doc.redeem_loyalty_points) {
			vmraid.call({
				method: "erpadda.accounts.doctype.loyalty_program.loyalty_program.get_loyalty_program_details",
				args: {
					"customer": frm.doc.customer,
					"loyalty_program": frm.doc.loyalty_program,
					"expiry_date": frm.doc.posting_date,
					"company": frm.doc.company
				},
				callback: function(r) {
					if (r) {
						frm.set_value("loyalty_redemption_account", r.message.expense_account);
						frm.set_value("loyalty_redemption_cost_center", r.message.cost_center);
						frm.redemption_conversion_factor = r.message.conversion_factor;
					}
				}
			});
		}
	},

	set_loyalty_points: function(frm) {
		if (frm.redemption_conversion_factor) {
			let loyalty_amount = flt(frm.redemption_conversion_factor*flt(frm.doc.loyalty_points), precision("loyalty_amount"));
			var remaining_amount = flt(frm.doc.grand_total) - flt(frm.doc.total_advance) - flt(frm.doc.write_off_amount);
			if (frm.doc.grand_total && (remaining_amount < loyalty_amount)) {
				let redeemable_points = parseInt(remaining_amount/frm.redemption_conversion_factor);
				vmraid.throw(__("You can only redeem max {0} points in this order.",[redeemable_points]));
			}
			frm.set_value("loyalty_amount", loyalty_amount);
		}
	},

	request_for_payment: function (frm) {
		if (!frm.doc.contact_mobile) {
			vmraid.throw(__('Please enter mobile number first.'));
		}
		frm.dirty();
		frm.save().then(() => {
			vmraid.dom.freeze(__('Waiting for payment...'));
			vmraid
				.call({
					method: 'create_payment_request',
					doc: frm.doc
				})
				.fail(() => {
					vmraid.dom.unfreeze();
					vmraid.msgprint(__('Payment request failed'));
				})
				.then(({ message }) => {
					const payment_request_name = message.name;
					setTimeout(() => {
						vmraid.db.get_value('Payment Request', payment_request_name, ['status', 'grand_total']).then(({ message }) => {
							if (message.status != 'Paid') {
								vmraid.dom.unfreeze();
								vmraid.msgprint({
									message: __('Payment Request took too long to respond. Please try requesting for payment again.'),
									title: __('Request Timeout')
								});
							} else if (vmraid.dom.freeze_count != 0) {
								vmraid.dom.unfreeze();
								cur_frm.reload_doc();
								cur_pos.payment.events.submit_invoice();

								vmraid.show_alert({
									message: __("Payment of {0} received successfully.", [format_currency(message.grand_total, frm.doc.currency, 0)]),
									indicator: 'green'
								});
							}
						});
					}, 60000);
				});
		});
	}
});