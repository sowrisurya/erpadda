from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("System Settings")
	ss = vmraid.get_doc("System Settings", "System Settings")
	ss.email_footer_address = vmraid.db.get_default("company")
	ss.flags.ignore_mandatory = True
	ss.save()
