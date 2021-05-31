from __future__ import unicode_literals
import vmraid

def execute():
	for d in vmraid.db.get_all("Stock Entry"):
		se = vmraid.get_doc("Stock Entry", d.name)
		se.set_total_incoming_outgoing_value()
		se.db_update()
