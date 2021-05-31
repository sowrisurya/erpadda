from __future__ import unicode_literals
import vmraid

def execute():
	for doctype in ("Sales Order", "Purchase Order"):
		for doc in vmraid.get_all(doctype, filters={"docstatus": 1}):
			doc = vmraid.get_doc(doctype, doc.name)
			doc.set_status(update=True)
