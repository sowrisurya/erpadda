from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("Email Digest")
	vmraid.db.sql("update `tabEmail Digest` set add_quote = 1")
