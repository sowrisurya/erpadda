from __future__ import unicode_literals
import vmraid

def execute():
	duplicates = vmraid.db.sql("""select email_group, email, count(name)
		from `tabEmail Group Member`
		group by email_group, email
		having count(name) > 1""")

	# delete all duplicates except 1
	for email_group, email, count in duplicates:
		vmraid.db.sql("""delete from `tabEmail Group Member`
			where email_group=%s and email=%s limit %s""", (email_group, email, count-1))
