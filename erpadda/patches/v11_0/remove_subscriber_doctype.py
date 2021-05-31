from __future__ import unicode_literals
import vmraid
from vmraid.model.utils.rename_field import rename_field

def execute():
	""" copy subscribe field to customer """
	vmraid.reload_doc("accounts","doctype","subscription")

	if vmraid.db.exists("DocType", "Subscriber"):
		if vmraid.db.has_column('Subscription','subscriber'):
			vmraid.db.sql("""
				update `tabSubscription` s1
				set customer=(select customer from tabSubscriber where name=s1.subscriber)
			""")

		vmraid.delete_doc("DocType", "Subscriber")