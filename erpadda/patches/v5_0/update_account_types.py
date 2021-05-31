# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	for company in vmraid.db.get_all("Company"):
		company = vmraid.get_doc("Company", company.name)

		match_types = ("Stock Received But Not Billed", "Stock Adjustment", "Expenses Included In Valuation",
			"Cost of Goods Sold")

		for account_type in match_types:
			account_name = "{0} - {1}".format(account_type, company.abbr)
			current_account_type = vmraid.db.get_value("Account", account_name, "account_type")
			if current_account_type != account_type:
				vmraid.db.set_value("Account", account_name, "account_type", account_type)

		company.set_default_accounts()
