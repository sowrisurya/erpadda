# -*- coding: utf-8 -*-
# Copyright (c) 2019, VMRaid Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import vmraid
import unittest
from vmraid.utils import set_request
from vmraid.website.render import render

class TestHomepage(unittest.TestCase):
	def test_homepage_load(self):
		set_request(method='GET', path='home')
		response = render()

		self.assertEqual(response.status_code, 200)

		html = vmraid.safe_decode(response.get_data())
		self.assertTrue('<section class="hero-section' in html)
