# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.utils import money_in_words

def execute():
	company_currency = dict(vmraid.db.sql("select name, default_currency from `tabCompany`"))
	bank_or_cash_accounts = vmraid.db.sql_list("""select name from `tabAccount`
		where account_type in ('Bank', 'Cash') and docstatus < 2""")

	for je in vmraid.db.sql_list("""select name from `tabJournal Entry` where docstatus < 2"""):
		total_amount = 0
		total_amount_in_words = ""

		je_doc = vmraid.get_doc('Journal Entry', je)
		for d in je_doc.get("accounts"):
			if (d.party_type and d.party) or d.account in bank_or_cash_accounts:
				total_amount = d.debit or d.credit
				if total_amount:
					total_amount_in_words = money_in_words(total_amount, company_currency.get(je_doc.company))

		if total_amount:
			vmraid.db.sql("""update `tabJournal Entry` set total_amount=%s, total_amount_in_words=%s
				where name = %s""", (total_amount, total_amount_in_words, je))
