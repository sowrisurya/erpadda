// Copyright (c) 2016, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

vmraid.query_reports["Expiring Memberships"] = {
	"filters": [
		{
			"fieldname": "fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"default": vmraid.defaults.get_user_default("fiscal_year"),
			"reqd": 1
		},
		{
			"fieldname":"month",
			"label": __("Month"),
			"fieldtype": "Select",
			"options": "Jan\nFeb\nMar\nApr\nMay\nJun\nJul\nAug\nSep\nOct\nNov\nDec",
			"default": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
				"Dec"][vmraid.datetime.str_to_obj(vmraid.datetime.get_today()).getMonth()],
		}
	]
}
