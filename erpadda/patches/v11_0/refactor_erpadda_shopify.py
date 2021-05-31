from __future__ import unicode_literals
import vmraid
from vmraid.installer import remove_from_installed_apps

def execute():
	vmraid.reload_doc('erpadda_integrations', 'doctype', 'shopify_settings')
	vmraid.reload_doc('erpadda_integrations', 'doctype', 'shopify_tax_account')
	vmraid.reload_doc('erpadda_integrations', 'doctype', 'shopify_log')
	vmraid.reload_doc('erpadda_integrations', 'doctype', 'shopify_webhook_detail')

	if 'erpadda_shopify' in vmraid.get_installed_apps():
		remove_from_installed_apps('erpadda_shopify')

		vmraid.delete_doc("Module Def", 'erpadda_shopify')

		vmraid.db.commit()

		vmraid.db.sql("truncate `tabShopify Log`")

		setup_app_type()
	else:
		disable_shopify()

def setup_app_type():
	try:
		shopify_settings = vmraid.get_doc("Shopify Settings")
		shopify_settings.app_type = 'Private'
		shopify_settings.update_price_in_erpadda_price_list = 0 if getattr(shopify_settings, 'push_prices_to_shopify', None) else 1
		shopify_settings.flags.ignore_mandatory = True
		shopify_settings.ignore_permissions = True
		shopify_settings.save()
	except Exception:
		vmraid.db.set_value("Shopify Settings", None, "enable_shopify", 0)
		vmraid.log_error(vmraid.get_traceback())

def disable_shopify():
	# due to vmraid.db.set_value wrongly written and enable_shopify being default 1
	# Shopify Settings isn't properly configured and leads to error
	shopify = vmraid.get_doc('Shopify Settings')

	if shopify.app_type == "Public" or shopify.app_type == None or \
		(shopify.enable_shopify and not (shopify.shopify_url or shopify.api_key)):
		vmraid.db.set_value("Shopify Settings", None, "enable_shopify", 0)
