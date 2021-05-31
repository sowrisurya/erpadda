from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("Contact")
	vmraid.db.sql("""update tabContact, tabUser set tabContact.user = tabUser.name
		where tabContact.email_id = tabUser.email""")
