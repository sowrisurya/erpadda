from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("stock", "doctype", "warehouse")
	vmraid.db.sql("""update tabWarehouse
		set is_group = if ((ifnull(is_group, "No") = "Yes" or ifnull(is_group, 0) = 1), 1, 0)""")