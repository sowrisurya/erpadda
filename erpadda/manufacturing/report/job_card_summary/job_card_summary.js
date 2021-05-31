// Copyright (c) 2016, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

vmraid.query_reports["Job Card Summary"] = {
	"filters": [
		{
			label: __("Company"),
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			default: vmraid.defaults.get_user_default("Company"),
			reqd: 1
		},
		{
			fieldname: "fiscal_year",
			label: __("Fiscal Year"),
			fieldtype: "Link",
			options: "Fiscal Year",
			default: vmraid.defaults.get_user_default("fiscal_year"),
			reqd: 1,
			on_change: function(query_report) {
				var fiscal_year = query_report.get_values().fiscal_year;
				if (!fiscal_year) {
					return;
				}
				vmraid.model.with_doc("Fiscal Year", fiscal_year, function(r) {
					var fy = vmraid.model.get_doc("Fiscal Year", fiscal_year);
					vmraid.query_report.set_filter_value({
						from_date: fy.year_start_date,
						to_date: fy.year_end_date
					});
				});
			}
		},
		{
			label: __("From Posting Date"),
			fieldname:"from_date",
			fieldtype: "Date",
			default: vmraid.defaults.get_user_default("year_start_date"),
			reqd: 1
		},
		{
			label: __("To Posting Date"),
			fieldname:"to_date",
			fieldtype: "Date",
			default: vmraid.defaults.get_user_default("year_end_date"),
			reqd: 1,
		},
		{
			label: __("Status"),
			fieldname: "status",
			fieldtype: "Select",
			options: ["", "Open", "Work In Progress", "Completed", "On Hold"]
		},
		{
			label: __("Sales Orders"),
			fieldname: "sales_order",
			fieldtype: "MultiSelectList",
			get_data: function(txt) {
				return vmraid.db.get_link_options('Sales Order', txt);
			}
		},
		{
			label: __("Production Item"),
			fieldname: "production_item",
			fieldtype: "MultiSelectList",
			get_data: function(txt) {
				return vmraid.db.get_link_options('Item', txt);
			}
		}
	]
};
