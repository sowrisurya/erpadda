// Copyright (c) 2016, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

vmraid.query_reports["Sales Partner Commission Summary"] = {
	"filters": [

		{
			fieldname: "sales_partner",
			label: __("Sales Partner"),
			fieldtype: "Link",
			options: "Sales Partner"
		},
		{
			fieldname: "doctype",
			label: __("Document Type"),
			fieldtype: "Select",
			options: "Sales Order\nDelivery Note\nSales Invoice",
			default: "Sales Order"
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: vmraid.datetime.add_months(vmraid.datetime.get_today(), -1),
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: vmraid.datetime.get_today()
		},
		{
			fieldname:"company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: vmraid.defaults.get_user_default("Company")
		},
		{
			fieldname:"customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer",
		},
		{
			fieldname:"territory",
			label: __("Territory"),
			fieldtype: "Link",
			options: "Territory",
		},

	]
}
