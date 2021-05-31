from __future__ import unicode_literals
import vmraid
from erpadda import get_default_currency

def execute():
	vmraid.reload_doc("accounts", "doctype", "journal_entry")

	vmraid.db.sql(""" update `tabJournal Entry` set total_amount_currency = %s
		where ifnull(multi_currency, 0) = 0
		and (pay_to_recd_from is not null or pay_to_recd_from != "") """, get_default_currency())

	for je in vmraid.db.sql(""" select name from `tabJournal Entry` where multi_currency = 1
		and (pay_to_recd_from is not null or pay_to_recd_from != "")""", as_dict=1):

		doc = vmraid.get_doc("Journal Entry", je.name)
		for d in doc.get('accounts'):
			if d.party_type and d.party:
				total_amount_currency = d.account_currency

			elif vmraid.db.get_value("Account", d.account, "account_type") in ["Bank", "Cash"]:
				total_amount_currency = d.account_currency

		vmraid.db.set_value("Journal Entry", je.name, "total_amount_currency",
			total_amount_currency, update_modified=False)
