# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals

import vmraid
import unittest
import json
from vmraid import _
from vmraid.utils import random_string
from erpadda.accounts.doctype.account.chart_of_accounts.chart_of_accounts import get_charts_for_country

test_ignore = ["Account", "Cost Center", "Payment Terms Template", "Salary Component", "Warehouse"]
test_dependencies = ["Fiscal Year"]
test_records = vmraid.get_test_records('Company')

class TestCompany(unittest.TestCase):
	def test_coa_based_on_existing_company(self):
		company = vmraid.new_doc("Company")
		company.company_name = "COA from Existing Company"
		company.abbr = "CFEC"
		company.default_currency = "INR"
		company.create_chart_of_accounts_based_on = "Existing Company"
		company.existing_company = "_Test Company"
		company.save()

		expected_results = {
			"Debtors - CFEC": {
				"account_type": "Receivable",
				"is_group": 0,
				"root_type": "Asset",
				"parent_account": "Accounts Receivable - CFEC",
			},
			"Cash - CFEC": {
				"account_type": "Cash",
				"is_group": 0,
				"root_type": "Asset",
				"parent_account": "Cash In Hand - CFEC"
			}
		}

		for account, acc_property in expected_results.items():
			acc = vmraid.get_doc("Account", account)
			for prop, val in acc_property.items():
				self.assertEqual(acc.get(prop), val)

		self.delete_mode_of_payment("COA from Existing Company")
		vmraid.delete_doc("Company", "COA from Existing Company")

	def test_coa_based_on_country_template(self):
		countries = ["Canada", "Germany", "France"]

		for country in countries:
			templates = get_charts_for_country(country)
			if len(templates) != 1 and "Standard" in templates:
				templates.remove("Standard")

			self.assertTrue(templates)

			for template in templates:
				try:
					company = vmraid.new_doc("Company")
					company.company_name = template
					company.abbr = random_string(3)
					company.default_currency = "USD"
					company.create_chart_of_accounts_based_on = "Standard Template"
					company.chart_of_accounts = template
					company.save()

					account_types = ["Cost of Goods Sold", "Depreciation",
						"Expenses Included In Valuation", "Fixed Asset", "Payable", "Receivable",
						"Stock Adjustment", "Stock Received But Not Billed", "Bank", "Cash", "Stock"]

					for account_type in account_types:
						filters = {
							"company": template,
							"account_type": account_type
						}
						if account_type in ["Bank", "Cash"]:
							filters["is_group"] = 1

						has_matching_accounts = vmraid.get_all("Account", filters)
						error_message = _("No Account matched these filters: {}").format(json.dumps(filters))

						self.assertTrue(has_matching_accounts, msg=error_message)
				finally:
					self.delete_mode_of_payment(template)
					vmraid.delete_doc("Company", template)

	def delete_mode_of_payment(self, company):
		vmraid.db.sql(""" delete from `tabMode of Payment Account`
			where company =%s """, (company))

def create_company_communication(doctype, docname):
	comm = vmraid.get_doc({
			"doctype": "Communication",
			"communication_type": "Communication",
			"content": "Deduplication of Links",
			"communication_medium": "Email",
			"reference_doctype":doctype,
			"reference_name":docname
		})
	comm.insert()

def create_child_company():
	child_company = vmraid.db.exists("Company", "Test Company")
	if not child_company:
		child_company = vmraid.get_doc({
			"doctype":"Company",
			"company_name":"Test Company",
			"abbr":"test_company",
			"default_currency":"INR"
		})
		child_company.insert()
	else:
		child_company = vmraid.get_doc("Company", child_company)

	return child_company.name

def create_test_lead_in_company(company):
	lead = vmraid.db.exists("Lead", "Test Lead in new company")
	if not lead:
		lead = vmraid.get_doc({
			"doctype": "Lead",
			"lead_name": "Test Lead in new company",
			"scompany": company
		})
		lead.insert()
	else:
		lead = vmraid.get_doc("Lead", lead)
		lead.company = company
		lead.save()
	return lead.name

