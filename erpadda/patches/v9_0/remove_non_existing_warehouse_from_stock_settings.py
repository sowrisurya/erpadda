from __future__ import unicode_literals
import vmraid

def execute():
	default_warehouse = vmraid.db.get_value("Stock Settings", None, "default_warehouse")
	if default_warehouse:
		if not vmraid.db.get_value("Warehouse", {"name": default_warehouse}):
			vmraid.db.set_value("Stock Settings", None, "default_warehouse", "")