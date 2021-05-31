# -*- coding: utf-8 -*-
# Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import vmraid
import unittest

class TestFertilizer(unittest.TestCase):
	def test_fertilizer_creation(self):
		self.assertEqual(vmraid.db.exists('Fertilizer', 'Urea'), 'Urea')