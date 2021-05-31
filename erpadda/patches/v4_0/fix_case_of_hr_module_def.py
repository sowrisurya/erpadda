# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors

from __future__ import unicode_literals
import vmraid

def execute():
	hr = vmraid.db.get_value("Module Def", "HR")
	if hr == "Hr":
		vmraid.rename_doc("Module Def", "Hr", "HR")
		vmraid.db.set_value("Module Def", "HR", "module_name", "HR")

	vmraid.clear_cache()
	vmraid.setup_module_map()
