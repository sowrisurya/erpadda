# -*- coding: utf-8 -*-
# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import vmraid
import unittest
from vmraid.utils import nowdate,flt, cstr,random_string
# test_records = vmraid.get_test_records('Vehicle')

class TestVehicle(unittest.TestCase):
	def test_make_vehicle(self):
		vehicle = vmraid.get_doc({
			"doctype": "Vehicle",
			"license_plate": random_string(10).upper(),
			"make": "Maruti",
			"model": "PCM",
			"last_odometer":5000,
			"acquisition_date":vmraid.utils.nowdate(),
			"location": "Mumbai",
			"chassis_no": "1234ABCD",
			"uom": "Litre",
			"vehicle_value":vmraid.utils.flt(500000)
		})
		vehicle.insert()
