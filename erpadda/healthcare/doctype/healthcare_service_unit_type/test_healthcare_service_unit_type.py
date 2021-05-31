# -*- coding: utf-8 -*-
# Copyright (c) 2018, VMRaid Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals
import unittest
import vmraid

class TestHealthcareServiceUnitType(unittest.TestCase):
	def test_item_creation(self):
		unit_type = get_unit_type()
		self.assertTrue(vmraid.db.exists('Item', unit_type.item))

		# check item disabled
		unit_type.disabled = 1
		unit_type.save()
		self.assertEqual(vmraid.db.get_value('Item', unit_type.item, 'disabled'), 1)


def get_unit_type():
	if vmraid.db.exists('Healthcare Service Unit Type', 'Inpatient Rooms'):
		return vmraid.get_doc('Healthcare Service Unit Type', 'Inpatient Rooms')

	unit_type = vmraid.new_doc('Healthcare Service Unit Type')
	unit_type.service_unit_type = 'Inpatient Rooms'
	unit_type.inpatient_occupancy = 1
	unit_type.is_billable = 1
	unit_type.item_code = 'Inpatient Rooms'
	unit_type.item_group = 'Services'
	unit_type.uom = 'Hour'
	unit_type.no_of_hours = 1
	unit_type.rate = 4000
	unit_type.save()
	return unit_type