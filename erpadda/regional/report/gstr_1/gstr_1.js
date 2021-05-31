// Copyright (c) 2018, VMRaid Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

vmraid.query_reports["GSTR-1"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1,
			"default": vmraid.defaults.get_user_default("Company")
		},
		{
			"fieldname": "company_address",
			"label": __("Address"),
			"fieldtype": "Link",
			"options": "Address",
			"get_query": function () {
				var company = vmraid.query_report.get_filter_value('company');
				if (company) {
					return {
						"query": 'vmraid.contacts.doctype.address.address.address_query',
						"filters": { link_doctype: 'Company', link_name: company }
					};
				}
			}
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": vmraid.datetime.add_months(vmraid.datetime.get_today(), -3),
			"width": "80"
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": vmraid.datetime.get_today()
		},
		{
			"fieldname": "type_of_business",
			"label": __("Type of Business"),
			"fieldtype": "Select",
			"reqd": 1,
			"options": ["B2B", "B2C Large", "B2C Small", "CDNR", "EXPORT"],
			"default": "B2B"
		}
	],
	onload: function (report) {

		report.page.add_inner_button(__("Download as JSON"), function () {
			var filters = report.get_values();

			vmraid.call({
				method: 'erpadda.regional.report.gstr_1.gstr_1.get_json',
				args: {
					data: report.data,
					report_name: report.report_name,
					filters: filters
				},
				callback: function(r) {
					if (r.message) {
						const args = {
							cmd: 'erpadda.regional.report.gstr_1.gstr_1.download_json_file',
							data: r.message.data,
							report_name: r.message.report_name,
							report_type: r.message.report_type
						};
						open_url_post(vmraid.request.url, args);
					}
				}
			});
		});
	}
}
