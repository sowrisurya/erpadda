# -*- coding: utf-8 -*-
# Copyright (c) 2019, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import vmraid
from vmraid import _
from vmraid.model.document import Document

class ItemManufacturer(Document):
	def validate(self):
		self.validate_duplicate_entry()
		self.manage_default_item_manufacturer()

	def on_trash(self):
		self.manage_default_item_manufacturer(delete=True)

	def validate_duplicate_entry(self):
		if self.is_new():
			filters = {
				'item_code': self.item_code,
				'manufacturer': self.manufacturer,
				'manufacturer_part_no': self.manufacturer_part_no
			}

			if vmraid.db.exists("Item Manufacturer", filters):
				vmraid.throw(_("Duplicate entry against the item code {0} and manufacturer {1}")
					.format(self.item_code, self.manufacturer))

	def manage_default_item_manufacturer(self, delete=False):
		from vmraid.model.utils import set_default

		item = vmraid.get_doc("Item", self.item_code)
		default_manufacturer = item.default_item_manufacturer
		default_part_no = item.default_manufacturer_part_no

		if not self.is_default:
			# if unchecked and default in Item master, clear it.
			if default_manufacturer == self.manufacturer and default_part_no == self.manufacturer_part_no:
				vmraid.db.set_value("Item", item.name,
					{
						"default_item_manufacturer": None,
						"default_manufacturer_part_no": None
					})

		elif self.is_default:
			set_default(self, "item_code")
			manufacturer, manufacturer_part_no = default_manufacturer, default_part_no

			if delete:
				manufacturer, manufacturer_part_no = None, None

			elif (default_manufacturer != self.manufacturer) or \
				(default_manufacturer == self.manufacturer and default_part_no != self.manufacturer_part_no):
				manufacturer = self.manufacturer
				manufacturer_part_no = self.manufacturer_part_no

			vmraid.db.set_value("Item", item.name,
					{
						"default_item_manufacturer": manufacturer,
						"default_manufacturer_part_no": manufacturer_part_no
					})

@vmraid.whitelist()
def get_item_manufacturer_part_no(item_code, manufacturer):
	return vmraid.db.get_value("Item Manufacturer",
		{'item_code': item_code, 'manufacturer': manufacturer}, 'manufacturer_part_no')