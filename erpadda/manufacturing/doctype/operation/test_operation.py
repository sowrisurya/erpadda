# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import vmraid
import unittest

test_records = vmraid.get_test_records('Operation')

class TestOperation(unittest.TestCase):
	pass

def make_operation(*args, **kwargs):
	args = args if args else kwargs
	if isinstance(args, tuple):
		args = args[0]

	args = vmraid._dict(args)

	try:
		doc = vmraid.get_doc({
			"doctype": "Operation",
			"name": args.operation,
			"workstation": args.workstation
		})

		doc.insert()

		return doc
	except vmraid.DuplicateEntryError:
		return vmraid.get_doc("Operation", args.operation)