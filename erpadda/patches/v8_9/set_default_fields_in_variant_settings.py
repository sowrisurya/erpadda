# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('stock', 'doctype', 'item_variant_settings')
	vmraid.reload_doc('stock', 'doctype', 'variant_field')

	doc = vmraid.get_doc('Item Variant Settings')
	doc.set_default_fields()
	doc.save()