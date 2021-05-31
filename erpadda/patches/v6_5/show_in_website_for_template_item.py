from __future__ import unicode_literals
import vmraid
import vmraid.website.render

def execute():
	for item_code in vmraid.db.sql_list("""select distinct variant_of from `tabItem`
		where variant_of is not null and variant_of !='' and show_in_website=1"""):

		item = vmraid.get_doc("Item", item_code)
		item.db_set("show_in_website", 1, update_modified=False)

		item.make_route()
		item.db_set("route", item.route, update_modified=False)

	vmraid.website.render.clear_cache()
