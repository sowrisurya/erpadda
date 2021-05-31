# -*- coding: utf-8 -*-
# Copyright (c) 2019, VMRaid Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import vmraid
import unittest


class TestQualityFeedback(unittest.TestCase):
	def test_quality_feedback(self):
		template = vmraid.get_doc(dict(
			doctype = 'Quality Feedback Template',
			template = 'Test Template',
			parameters = [
				dict(parameter='Test Parameter 1'),
				dict(parameter='Test Parameter 2')
			]
		)).insert()

		feedback = vmraid.get_doc(dict(
			doctype = 'Quality Feedback',
			template = template.name,
			document_type = 'User',
			document_name = vmraid.session.user
		)).insert()

		self.assertEqual(template.parameters[0].parameter, feedback.parameters[0].parameter)

		feedback.delete()
		template.delete()
