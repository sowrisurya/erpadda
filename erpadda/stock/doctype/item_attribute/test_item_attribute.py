# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors and Contributors
# See license.txt

from __future__ import unicode_literals
import vmraid
import unittest

test_records = vmraid.get_test_records('Item Attribute')

from erpadda.stock.doctype.item_attribute.item_attribute import ItemAttributeIncrementError

class TestItemAttribute(unittest.TestCase):
	def setUp(self):
		if vmraid.db.exists("Item Attribute", "_Test_Length"):
			vmraid.delete_doc("Item Attribute", "_Test_Length")

	def test_numeric_item_attribute(self):
		item_attribute = vmraid.get_doc({
			"doctype": "Item Attribute",
			"attribute_name": "_Test_Length",
			"numeric_values": 1,
			"from_range": 0.0,
			"to_range": 100.0,
			"increment": 0
		})

		self.assertRaises(ItemAttributeIncrementError, item_attribute.save)

		item_attribute.increment = 0.5
		item_attribute.save()

