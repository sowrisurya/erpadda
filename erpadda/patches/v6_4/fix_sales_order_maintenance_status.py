from __future__ import unicode_literals
import vmraid

def execute():
	for doc in vmraid.get_all("Sales Order", filters={"docstatus": 1,
		"order_type": "Maintenance"}):
		doc = vmraid.get_doc("Sales Order", doc.name)
		doc.set_status(update=True)
