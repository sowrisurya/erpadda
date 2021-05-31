from __future__ import unicode_literals
import vmraid

def execute():
	for company in vmraid.get_all("Company",
			["name", "default_receivable_account", "default_payable_account"]):

		if company.default_receivable_account:
			vmraid.db.sql("""update `tabSales Invoice` invoice set `debit_to`=%(account)s
				where company=%(company)s
				and not exists (select name from `tabAccount` account where account.name=invoice.debit_to)""",
				{"company": company.name, "account": company.default_receivable_account})

		if company.default_payable_account:
			vmraid.db.sql("""update `tabPurchase Invoice` invoice set `credit_to`=%(account)s
				where company=%(company)s
				and not exists (select name from `tabAccount` account where account.name=invoice.credit_to)""",
				{"company": company.name, "account": company.default_payable_account})
