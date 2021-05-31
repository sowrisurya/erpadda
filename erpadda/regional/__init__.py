# Copyright (c) 2018, VMRaid Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid import _
from erpadda import get_region

def check_deletion_permission(doc, method):
	region = get_region(doc.company)
	if region in ["Nepal", "France"] and doc.docstatus != 0:
		vmraid.throw(_("Deletion is not permitted for country {0}").format(region))

def create_transaction_log(doc, method):
	"""
	Appends the transaction to a chain of hashed logs for legal resons.
	Called on submit of Sales Invoice and Payment Entry.
	"""
	region = get_region()
	if region not in ["France", "Germany"]:
		return

	data = str(doc.as_dict())

	vmraid.get_doc({
		"doctype": "Transaction Log",
		"reference_doctype": doc.doctype,
		"document_name": doc.name,
		"data": data
	}).insert(ignore_permissions=True)