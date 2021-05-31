from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('accounts', 'doctype', 'bank', force=1)

	if vmraid.db.table_exists('Bank') and vmraid.db.table_exists('Bank Account') and vmraid.db.has_column('Bank Account', 'swift_number'):
		vmraid.db.sql("""
			UPDATE `tabBank` b, `tabBank Account` ba
			SET b.swift_number = ba.swift_number WHERE b.name = ba.bank
		""")

	vmraid.reload_doc('accounts', 'doctype', 'bank_account')
	vmraid.reload_doc('accounts', 'doctype', 'payment_request')
