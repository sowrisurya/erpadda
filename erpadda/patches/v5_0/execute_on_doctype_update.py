# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	for dt in ("Stock Ledger Entry", "Communication", "DefaultValue", "DocShare", "File", "ToDo"):
		vmraid.get_doc("DocType", dt).run_module_method("on_doctype_update")
