from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('stock', 'doctype', 'item')
	vmraid.db.sql("""update `tabItem` set publish_in_hub = 0""")
