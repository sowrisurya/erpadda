// Copyright (c) 2016, ESS
// License: See license.txt

vmraid.query_reports["Lab Test Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": vmraid.datetime.add_months(vmraid.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": vmraid.datetime.now_date(),
			"reqd": 1
		},
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"default": vmraid.defaults.get_default("Company"),
			"options": "Company"
		},
		{
			"fieldname": "template",
			"label": __("Lab Test Template"),
			"fieldtype": "Link",
			"options": "Lab Test Template"
		},
		{
			"fieldname": "patient",
			"label": __("Patient"),
			"fieldtype": "Link",
			"options": "Patient"
		},
		{
			"fieldname": "department",
			"label": __("Medical Department"),
			"fieldtype": "Link",
			"options": "Medical Department"
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "\nCompleted\nApproved\nRejected"
		},
		{
			"fieldname": "invoiced",
			"label": __("Invoiced"),
			"fieldtype": "Check"
		}
	]
};
