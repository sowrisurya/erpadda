from __future__ import unicode_literals
import vmraid
import vmraid.model

def execute():
	vmraid.reload_doc("setup", "doctype", "item_group")
	vmraid.reload_doc("stock", "doctype", "item")
	vmraid.reload_doc("setup", "doctype", "sales_partner")
	
	try:
		vmraid.model.rename_field("Item Group", "parent_website_sitemap", "parent_website_route")
		vmraid.model.rename_field("Item", "parent_website_sitemap", "parent_website_route")
		vmraid.model.rename_field("Sales Partner", "parent_website_sitemap",
			 "parent_website_route")
	except Exception as e:
		if e.args[0]!=1054:
			raise
