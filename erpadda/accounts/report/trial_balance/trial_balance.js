// Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

vmraid.require("assets/erpadda/js/financial_statements.js", function() {
	vmraid.query_reports["Trial Balance"] = {
		"filters": [
			{
				"fieldname": "company",
				"label": __("Company"),
				"fieldtype": "Link",
				"options": "Company",
				"default": vmraid.defaults.get_user_default("Company"),
				"reqd": 1
			},
			{
				"fieldname": "fiscal_year",
				"label": __("Fiscal Year"),
				"fieldtype": "Link",
				"options": "Fiscal Year",
				"default": vmraid.defaults.get_user_default("fiscal_year"),
				"reqd": 1,
				"on_change": function(query_report) {
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
				"fieldname": "from_date",
				"label": __("From Date"),
				"fieldtype": "Date",
				"default": vmraid.defaults.get_user_default("year_start_date"),
			},
			{
				"fieldname": "to_date",
				"label": __("To Date"),
				"fieldtype": "Date",
				"default": vmraid.defaults.get_user_default("year_end_date"),
			},
			{
				"fieldname": "cost_center",
				"label": __("Cost Center"),
				"fieldtype": "Link",
				"options": "Cost Center",
				"get_query": function() {
					var company = vmraid.query_report.get_filter_value('company');
					return {
						"doctype": "Cost Center",
						"filters": {
							"company": company,
						}
					}
				}
			},
			{
				"fieldname": "project",
				"label": __("Project"),
				"fieldtype": "Link",
				"options": "Project"
			},
			{
				"fieldname": "finance_book",
				"label": __("Finance Book"),
				"fieldtype": "Link",
				"options": "Finance Book",
			},
			{
				"fieldname": "presentation_currency",
				"label": __("Currency"),
				"fieldtype": "Select",
				"options": erpadda.get_presentation_currency_list()
			},
			{
				"fieldname": "with_period_closing_entry",
				"label": __("Period Closing Entry"),
				"fieldtype": "Check",
				"default": 1
			},
			{
				"fieldname": "show_zero_values",
				"label": __("Show zero values"),
				"fieldtype": "Check"
			},
			{
				"fieldname": "show_unclosed_fy_pl_balances",
				"label": __("Show unclosed fiscal year's P&L balances"),
				"fieldtype": "Check"
			},
			{
				"fieldname": "include_default_book_entries",
				"label": __("Include Default Book Entries"),
				"fieldtype": "Check",
				"default": 1
			}
		],
		"formatter": erpadda.financial_statements.formatter,
		"tree": true,
		"name_field": "account",
		"parent_field": "parent_account",
		"initial_depth": 3
	}

	erpadda.utils.add_dimensions('Trial Balance', 6);
});


