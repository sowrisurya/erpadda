from __future__ import unicode_literals
import vmraid

from erpadda.setup.install import create_compact_item_print_custom_field

def execute():
	create_compact_item_print_custom_field()
	vmraid.db.set_value("Print Settings", None, "compact_item_print", 1)
