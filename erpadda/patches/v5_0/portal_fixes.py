from __future__ import unicode_literals
import vmraid
import erpadda.setup.install

def execute():
	vmraid.reload_doc("website", "doctype", "web_form_field", force=True, reset_permissions=True)
	#erpadda.setup.install.add_web_forms()
