// Copyright (c) 2016, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

vmraid.query_reports["Subcontracted Raw Materials To Be Transferred"] = {
	"filters": [
		{
			fieldname: "supplier",
			label: __("Supplier"),
			fieldtype: "Link",
			options: "Supplier",
			reqd: 1
		},
		{
			fieldname:"from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: vmraid.datetime.add_months(vmraid.datetime.month_start(), -1),
			reqd: 1
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: vmraid.datetime.add_days(vmraid.datetime.month_start(),-1),
			reqd: 1
		},
	]
}
