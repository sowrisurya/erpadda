from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('hub_node', 'doctype', 'Marketplace Settings')
	vmraid.db.set_value('Marketplace Settings', 'Marketplace Settings', 'marketplace_url', 'https://hubmarket.org')
