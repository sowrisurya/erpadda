from __future__ import unicode_literals
import vmraid
from vmraid import _
from vmraid.model.rename_doc import rename_doc

def execute():
	vmraid.reload_doc('stock', 'doctype', 'item')
	language = vmraid.get_single("System Settings").language

	if language and language.startswith('en'): return

	vmraid.local.lang = language

	all_domains = vmraid.get_hooks("domains")

	for domain in all_domains:
		translated_domain = _(domain, lang=language)
		if vmraid.db.exists("Domain", translated_domain):
			#if domain already exists merged translated_domain and domain
			merge = False
			if vmraid.db.exists("Domain", domain):
				merge=True

			rename_doc("Domain", translated_domain, domain, ignore_permissions=True, merge=merge)

	domain_settings = vmraid.get_single("Domain Settings")
	active_domains = [d.domain for d in domain_settings.active_domains]

	try:
		for domain in active_domains:
			domain = vmraid.get_doc("Domain", domain)
			domain.setup_domain()

			if int(vmraid.db.get_single_value('System Settings', 'setup_complete')):
				domain.setup_sidebar_items()
				domain.setup_desktop_icons()
				domain.set_default_portal_role()
	except vmraid.LinkValidationError:
		pass