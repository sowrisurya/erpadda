from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('erpadda_integrations', 'doctype', 'shopify_settings')
	vmraid.db.set_value('Shopify Settings', None, 'app_type', 'Private')